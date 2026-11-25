"""Penyimpanan data META.PORTAL versi web (diperkeras)."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

try:                      # Linux / macOS (PythonAnywhere)
    import fcntl
except ImportError:       # Windows
    fcntl = None
    try:
        import msvcrt
    except ImportError:
        msvcrt = None

USERNAME_RE = re.compile(r"[A-Za-z0-9_]{3,20}")
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
ROOM_ID_RE = re.compile(r"[A-Za-z0-9_-]{1,40}")
RESERVED_USERNAMES = {"admin", "administrator", "root", "system", "moderator", "staff", "guest", "support"}
MIN_PASSWORD_LEN, MAX_PASSWORD_LEN = 6, 128
NEW_ITER = 600_000        # rekomendasi OWASP untuk PBKDF2-HMAC-SHA256
LEGACY_ITER = 120_000     # akun lama yang belum punya field "iter"
_DUMMY_SALT = os.urandom(16)


class StoreError(Exception):
    """Berkas data tidak bisa dibaca dengan aman (rusak / tidak bisa diakses)."""


# ----------------------------------------------------------------------------- berkas
_THREAD_LOCKS: dict[str, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()


@contextmanager
def _file_lock(path: Path):
    lock_path = path.with_name(path.name + ".lock")
    with _THREAD_LOCKS_GUARD:
        tlock = _THREAD_LOCKS.setdefault(str(lock_path), threading.RLock())
    with tlock:
        fh = None
        locked = False
        try:
            fh = open(lock_path, "a+")
            fh.seek(0)
            if fcntl is not None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
                locked = True
            elif msvcrt is not None:
                msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
                locked = True
        except OSError:
            pass
        try:
            yield
        finally:
            if fh is not None:
                try:
                    if locked and fcntl is not None:
                        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
                    elif locked and msvcrt is not None:
                        fh.seek(0)
                        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
                fh.close()


def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{secrets.token_hex(4)}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class _JsonStore:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.data: dict = self._load()

    def _load(self) -> dict:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return {}
        except OSError as e:
            raise StoreError(f"Tidak bisa membaca {self.path.name}") from e
        try:
            data = json.loads(raw)
        except ValueError as e:
            raise StoreError(f"{self.path.name} rusak (JSON tidak valid); tidak ditimpa") from e
        if not isinstance(data, dict):
            raise StoreError(f"{self.path.name} berformat tidak dikenal")
        return data

    @contextmanager
    def _locked(self):
        with _file_lock(self.path):
            self.data = self._load()
            yield

    def _commit(self, ok_msg: str = "Berhasil disimpan.") -> tuple[bool, str]:
        try:
            _atomic_write(self.path, json.dumps(self.data, indent=2, ensure_ascii=False))
            return True, ok_msg
        except OSError:
            return False, "Gagal menyimpan data."


# ----------------------------------------------------------------------------- akun
def _hash(password: str, salt: bytes, iterations: int) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()


class UserStore(_JsonStore):
    @property
    def users(self) -> dict:
        return self.data

    @staticmethod
    def _pw_ok(pwd: str) -> bool:
        return MIN_PASSWORD_LEN <= len(pwd) <= MAX_PASSWORD_LEN

    def register(self, username: str, email: str, password: str, favorite_team: str = "None") -> tuple[bool, str]:
        username, email = username.strip(), email.strip()
        if not USERNAME_RE.fullmatch(username):
            return False, "Username 3-20 karakter: hanya huruf, angka, dan underscore."
        if username.lower() in RESERVED_USERNAMES:
            return False, "Username tersebut tidak tersedia."
        if not EMAIL_RE.fullmatch(email) or len(email) > 254:
            return False, "Format email tidak valid."
        if not self._pw_ok(password):
            return False, f"Password harus {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} karakter."
        salt = os.urandom(16)
        digest = _hash(password, salt, NEW_ITER)
        key = username.lower()
        with self._locked():
            if key in self.data or any(u.get("email", "").lower() == email.lower() for u in self.data.values()):
                return False, "Username atau email sudah terdaftar."
            self.data[key] = {
                "username": username, "email": email, "salt": salt.hex(), "hash": digest, "iter": NEW_ITER,
                "favorite_team": favorite_team, "created_at": datetime.now().strftime("%d %b %Y"),
            }
            return self._commit("Akun berhasil dibuat.")

    def _verify(self, user: dict, password: str) -> bool:
        if not self._pw_ok_len(password):
            return False
        it = int(user.get("iter", LEGACY_ITER))
        return hmac.compare_digest(user["hash"], _hash(password, bytes.fromhex(user["salt"]), it))

    @staticmethod
    def _pw_ok_len(pwd: str) -> bool:
        return 0 < len(pwd) <= MAX_PASSWORD_LEN

    def authenticate(self, username: str, password: str) -> bool:
        key = username.strip().lower()
        user = self.data.get(key)
        if user is None or not self._pw_ok_len(password):
            _hash(password[:MAX_PASSWORD_LEN] or "x", _DUMMY_SALT, NEW_ITER)
            return False
        ok = self._verify(user, password)
        if ok and int(user.get("iter", LEGACY_ITER)) < NEW_ITER:
            self._upgrade(key, password, user["hash"])
        return ok

    def _upgrade(self, key: str, password: str, old_hash: str) -> None:
        try:
            with self._locked():
                user = self.data.get(key)
                if not user or user["hash"] != old_hash:
                    return
                user["hash"] = _hash(password, bytes.fromhex(user["salt"]), NEW_ITER)
                user["iter"] = NEW_ITER
                self._commit()
        except StoreError:
            pass

    def get_user(self, username: str) -> dict | None:
        user = self.data.get(username.strip().lower())
        if not user:
            return None
        return {"username": user["username"], "email": user.get("email", ""),
                "favorite_team": user.get("favorite_team", "None"),
                "created_at": user.get("created_at", "")}

    def update_profile(self, username: str, email: str, favorite_team: str) -> tuple[bool, str]:
        key, email = username.strip().lower(), email.strip()
        if not EMAIL_RE.fullmatch(email) or len(email) > 254:
            return False, "Format email tidak valid."
        with self._locked():
            if key not in self.data:
                return False, "Pengguna tidak ditemukan."
            for k, u in self.data.items():
                if k != key and u.get("email", "").lower() == email.lower():
                    return False, "Email sudah dipakai oleh akun lain."
            self.data[key]["email"] = email
            self.data[key]["favorite_team"] = favorite_team
            return self._commit("Profil berhasil diperbarui.")

    def change_password(self, username: str, old_pwd: str, new_pwd: str) -> tuple[bool, str]:
        key = username.strip().lower()
        user = self.data.get(key)
        if not user:
            return False, "Pengguna tidak ditemukan."
        if not self._verify(user, old_pwd):
            return False, "Password saat ini salah."
        if not self._pw_ok(new_pwd):
            return False, f"Password baru harus {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} karakter."
        if old_pwd == new_pwd:
            return False, "Password baru tidak boleh sama dengan password lama."
        old_hash = user["hash"]
        salt = os.urandom(16)
        digest = _hash(new_pwd, salt, NEW_ITER)
        with self._locked():
            user = self.data.get(key)
            if not user or user["hash"] != old_hash:
                return False, "Data akun berubah, silakan ulangi."
            user.update(salt=salt.hex(), hash=digest, iter=NEW_ITER)
            return self._commit("Password berhasil diperbarui.")


# ----------------------------------------------------------------------------- pesan
class MessageStore(_JsonStore):
    @staticmethod
    def _defaults(username: str) -> list[dict]:
        now = datetime.now().strftime("%d %b %Y, %H:%M")
        mk = lambda sender, title, body, date, read, cat: {
            "id": uuid.uuid4().hex[:8], "sender": sender, "title": title, "body": body,
            "date": date, "read": read, "category": cat}
        return [
            mk("Sistem META.PORTAL", "Selamat Datang di META.PORTAL!",
               f"Halo {username}, selamat datang di META.PORTAL! Di sini kamu bisa memantau jadwal pertandingan "
               "esports, membaca berita terbaru, dan mengelola profil akunmu.", now, False, "System"),
            mk("Turnamen Hub", "Pengingat: Jadwal Match VCT Mendatang",
               "Pertandingan seru antara Paper Rex dan NRG akan segera berlangsung akhir pekan ini. "
               "Jangan lewatkan siaran langsung dan dukung tim favoritmu!", now, False, "Match"),
            mk("Komunitas Esports", "Tips Keamanan Akun",
               "Pastikan kamu menggunakan password yang kuat dan mengupdate tim favorit di tab profil untuk "
               "mendapatkan berita yang sesuai.", "30 Oct 2026, 14:20", True, "Security"),
        ]

    def get_messages(self, username: str) -> list[dict]:
        key = username.strip().lower()
        with self._locked():
            if key not in self.data:
                self.data[key] = self._defaults(username)
                self._commit()
            return [dict(m) for m in self.data[key]]

    def get_unread_count(self, username: str) -> int:
        return sum(1 for m in self.get_messages(username) if not m.get("read"))

    def set_read(self, username: str, msg_id: str, read: bool) -> bool:
        self.get_messages(username)
        with self._locked():
            for m in self.data.get(username.strip().lower(), []):
                if m.get("id") == msg_id:
                    m["read"] = bool(read)
                    return self._commit()[0]
        return False

    def mark_all_as_read(self, username: str) -> bool:
        self.get_messages(username)
        with self._locked():
            for m in self.data.get(username.strip().lower(), []):
                m["read"] = True
            return self._commit()[0]

    def delete_message(self, username: str, msg_id: str) -> bool:
        key = username.strip().lower()
        with self._locked():
            before = self.data.get(key, [])
            after = [m for m in before if m.get("id") != msg_id]
            if len(after) == len(before):
                return False
            self.data[key] = after
            return self._commit()[0]


# ----------------------------------------------------------------------------- forum & pickem
class ForumStore(_JsonStore):
    @staticmethod
    def _defaults() -> list[dict]:
        return [
            {
                "id": "th-1",
                "title": "Prx train?",
                "author": "Syctiz",
                "replies_count": 4,
                "comments": [
                    {"author": "Pelix", "text": "We are going choo choo", "time": "8 Minutes ago"},
                    {"author": "MARS", "text": "nahh the trains stop here", "time": "6 Minutes ago"},
                    {"author": "Hakari", "text": "Ofc, prx are fraud", "time": "4 Minutes ago", "reply_to": "MARS"},
                    {"author": "oseano", "text": "WE WILL DESTORY EVERYBODY ELSE, WE WILL DESTROY LONDON", "time": "5 Minutes ago"}
                ]
            },
            {
                "id": "th-2",
                "title": "Will EMEA be fraud?",
                "author": "Kazuma",
                "replies_count": 18,
                "comments": [
                    {"author": "Connor", "text": "Fnatic will carry the whole region as usual.", "time": "15 Minutes ago"}
                ]
            },
            {
                "id": "th-3",
                "title": "CHINA NUMBER 1 WE WILL TAKE OVER THE WORLD!!!",
                "author": "maRs",
                "replies_count": 25,
                "comments": [
                    {"author": "EDG_Fan", "text": "EDG and BLG are taking it all this year!", "time": "20 Minutes ago"}
                ]
            },
            {
                "id": "th-4",
                "title": "Will C9 miracle continues?",
                "author": "Linardeeeeeese",
                "replies_count": 9,
                "comments": [
                    {"author": "NA_Hope", "text": "Believe in the boys in blue!", "time": "30 Minutes ago"}
                ]
            },
            {
                "id": "th-5",
                "title": "This is the most boring masters ever..",
                "author": "Shield",
                "replies_count": 34,
                "comments": [
                    {"author": "ValorantEnthusiast", "text": "Wait until playoffs start, Swiss stage is just warming up.", "time": "1 hour ago"}
                ]
            },
            {
                "id": "th-6",
                "title": "RRQ slams all teams",
                "author": "cmaEv0s",
                "replies_count": 40,
                "comments": [
                    {"author": "KingRRQ", "text": "Pacific supremacy is inevitable.", "time": "2 hours ago"}
                ]
            },
            {
                "id": "th-7",
                "title": "Hi",
                "author": "oseano",
                "replies_count": 3,
                "comments": [
                    {"author": "Admin", "text": "Welcome to META.PORTAL community forum!", "time": "3 hours ago"}
                ]
            }
        ]

    def _ensure_threads(self):
        if "threads" not in self.data:
            self.data["threads"] = self._defaults()
            self._commit()

    def get_all(self, query: str = "") -> list[dict]:
        with self._locked():
            self._ensure_threads()
            threads = self.data.get("threads", [])
            if not query:
                return list(threads)
            q = query.lower()
            return [t for t in threads if q in t["title"].lower() or q in t["author"].lower()]

    def get_thread(self, thread_id: str) -> dict | None:
        with self._locked():
            self._ensure_threads()
            for t in self.data.get("threads", []):
                if t["id"] == thread_id:
                    return dict(t)
            return None

    def create_thread(self, title: str, content: str, author: str) -> dict:
        t_id = f"th-{uuid.uuid4().hex[:6]}"
        with self._locked():
            self._ensure_threads()
            new_th = {
                "id": t_id,
                "title": title.strip()[:100],
                "author": author.strip()[:30] or "Guest",
                "replies_count": 1 if content.strip() else 0,
                "comments": [
                    {"author": author.strip()[:30] or "Guest", "text": content.strip()[:1000], "time": "Just now"}
                ] if content.strip() else []
            }
            self.data["threads"].insert(0, new_th)
            self._commit()
            return new_th

    def add_comment(self, thread_id: str, author: str, text: str) -> bool:
        with self._locked():
            self._ensure_threads()
            for t in self.data.get("threads", []):
                if t["id"] == thread_id:
                    t["comments"].append({
                        "author": author.strip()[:30] or "Guest",
                        "text": text.strip()[:1000],
                        "time": "Just now"
                    })
                    t["replies_count"] = len(t["comments"])
                    self._commit()
                    return True
            return False


class PickemStore(_JsonStore):
    def get_user_pickem(self, username: str) -> dict:
        key = username.strip().lower()
        with self._locked():
            return dict(self.data.get(key, {}))

    def save_user_pickem(self, username: str, picks: dict):
        key = username.strip().lower()
        with self._locked():
            self.data[key] = {
                "picks": picks,
                "saved_at": datetime.now().strftime("%d %b %Y, %H:%M"),
                "score": 300
            }
            self._commit()


# ----------------------------------------------------------------------------- live chat (per match room)
class LiveChatStore(_JsonStore):
    DEFAULT_ROOM = "blg-vs-tl"

    @staticmethod
    def _normalize_room(match_id: str | None) -> str:
        if not match_id:
            return LiveChatStore.DEFAULT_ROOM
        cleaned = match_id.strip().lower()
        if ROOM_ID_RE.fullmatch(cleaned):
            return cleaned
        return LiveChatStore.DEFAULT_ROOM

    @staticmethod
    def _defaults(room_id: str) -> list[dict]:
        if room_id == LiveChatStore.DEFAULT_ROOM:
            return [
                {"id": "cmsg-1", "sender": "Connor", "msg": "When does Sentinel plays?", "time": "18:30"},
                {"id": "cmsg-2", "sender": "Ikuyo Kita", "msg": "Can't wait for BLG stomp TL", "time": "18:31"},
                {"id": "cmsg-3", "sender": "Goldship", "msg": "hey guys", "time": "18:32"},
                {"id": "cmsg-4", "sender": "Gigguk", "msg": "What's your pred goldship?", "time": "18:33"},
                {"id": "cmsg-5", "sender": "Kazuma", "msg": "is it just us in here?", "time": "18:34"},
            ]
        return [
            {
                "id": f"cmsg-{uuid.uuid4().hex[:8]}",
                "sender": "META Bot",
                "msg": f"Selamat datang di Live Match Chat ({room_id.upper()})!",
                "time": datetime.now().strftime("%H:%M"),
            }
        ]

    def _ensure_room(self, room_id: str) -> list[dict]:
        dirty = False
        if not isinstance(self.data.get("rooms"), dict):
            self.data["rooms"] = {}
            dirty = True

        # Migrasi otomatis jika masih ada struktur lama self.data["messages"]
        if isinstance(self.data.get("messages"), list):
            legacy_msgs = self.data.pop("messages")
            if legacy_msgs and self.DEFAULT_ROOM not in self.data["rooms"]:
                self.data["rooms"][self.DEFAULT_ROOM] = legacy_msgs
            dirty = True

        if room_id not in self.data["rooms"] or not isinstance(self.data["rooms"][room_id], list):
            self.data["rooms"][room_id] = self._defaults(room_id)
            dirty = True

        if dirty:
            self._commit()
        return self.data["rooms"][room_id]

    def get_messages(self, match_id: str | None = None, since_id: str | None = None, limit: int = 100) -> list[dict]:
        room_id = self._normalize_room(match_id)
        with self._locked():
            msgs = self._ensure_room(room_id)
            if not since_id:
                return [dict(m) for m in msgs[-limit:]]
            idx = -1
            for i, m in enumerate(msgs):
                if m.get("id") == since_id:
                    idx = i
            if idx != -1:
                return [dict(m) for m in msgs[idx + 1:]]
            return [dict(m) for m in msgs[-limit:]]

    def add_message(self, sender: str, msg: str, match_id: str | None = None) -> dict:
        room_id = self._normalize_room(match_id)
        text_clean = msg.strip()[:300]
        if not text_clean:
            raise ValueError("Pesan tidak boleh kosong.")
        now_str = datetime.now().strftime("%H:%M")
        msg_id = f"cmsg-{uuid.uuid4().hex[:8]}"
        new_msg = {
            "id": msg_id,
            "sender": sender.strip()[:30] or "Guest",
            "msg": text_clean,
            "time": now_str,
        }
        with self._locked():
            msgs = self._ensure_room(room_id)
            msgs.append(new_msg)
            if len(msgs) > 500:
                self.data["rooms"][room_id] = msgs[-500:]
            self._commit()
            return dict(new_msg)
