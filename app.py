"""META.PORTAL versi web (Flask), diperkeras. Lokal: python app.py -> http://127.0.0.1:5000

Variabel lingkungan (semua opsional):
  DATA_DIR       folder users.json / messages.json / secret.key (sebaiknya di luar folder aplikasi)
  SECRET_KEY     kunci sesi; kalau kosong dibuat otomatis di DATA_DIR/secret.key (izin 600)
  PROD=1         aktifkan cookie Secure dan HSTS (wajib di server HTTPS)
  TRUSTED_PROXY=1  percayai header X-Forwarded-For (PythonAnywhere berada di belakang proxy)
  FLASK_DEBUG=1  mode debug (hanya untuk lokal)
"""
from __future__ import annotations

import hashlib
import hmac
import math
import os
import secrets
import threading
import time
from collections import defaultdict, deque
from datetime import timedelta
from functools import wraps
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from web_models import (
    EMAIL_RE, MAX_PASSWORD_LEN, MIN_PASSWORD_LEN, USERNAME_RE,
    ForumStore, MessageStore, PickemStore, LiveChatStore, StoreError, UserStore
)
from portal_data import (
    DETAILED_MATCH_T1_PRX, LIVE_WATCH_MATCH, MASTER_SANTIAGO_DATA,
    NEWS_ARTICLES, PLAYER_F0RSAKEN, RESULT_MATCHES_LIST,
    STATS_PLAYERS_DATA, TEAM_PAPER_REX, UPCOMING_MATCHES_LIST,
    get_watch_match
)

BASE = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE))
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROD = os.environ.get("PROD") == "1"


def _load_secret_key() -> str:
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    key_file = DATA_DIR / "secret.key"
    if not key_file.exists():
        try:
            fd = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write(secrets.token_hex(32))
        except FileExistsError:
            pass
    try:
        os.chmod(key_file, 0o600)
    except OSError:
        pass
    return key_file.read_text().strip()


app = Flask(__name__)
app.secret_key = _load_secret_key()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=PROD,
    MAX_CONTENT_LENGTH=16 * 1024,
)
if os.environ.get("TRUSTED_PROXY") == "1":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# ------------------------------------------------------------------ sesi
SERVER_BOOT_ID = secrets.token_hex(8)
IDLE_TIMEOUT_SECONDS = 15 * 60
ABSOLUTE_TIMEOUT_SECONDS = 2 * 3600
app.permanent_session_lifetime = timedelta(seconds=ABSOLUTE_TIMEOUT_SECONDS)

USERS_FILE = DATA_DIR / "users.json"
MESSAGES_FILE = DATA_DIR / "messages.json"
FORUM_FILE = DATA_DIR / "forum.json"
PICKEM_FILE = DATA_DIR / "pickems.json"
CHAT_FILE = DATA_DIR / "live_chat.json"

NEWS = ['DRX Calls up academy teams player "yong" to main rosters', "M80 Statement",
        "Nongshim Red Force make a legendary history", "Paper Rex dominates NRG",
        'FunPlusPhoenix sign "Sacy" to the squad', "Tenz retirement"]
NEWS_SLUG_MAP = {
    'DRX Calls up academy teams player "yong" to main rosters': "drx-calls-up-yong",
    "M80 Statement": "m80-statement",
    "Nongshim Red Force make a legendary history": "nongshim-red-force-history",
    "Paper Rex dominates NRG": "paper-rex-dominates-nrg",
    'FunPlusPhoenix sign "Sacy" to the squad': "funplusphoenix-sign-sacy",
    "Tenz retirement": "tenz-retirement"
}
MATCHES = [("BLG", "TL", "Sat, 25 Oct"), ("RRQ", "T1", "Sat, 25 Oct"), ("C9", "PRX", "Sun, 26 Oct"),
           ("VIT", "NRG", "Sun, 26 Oct"), ("WOL", "EDG", "Mon, 27 Oct"), ("FPX", "AG", "Mon, 27 Oct"),
           ("VKS", "GEN", "Tue, 28 Oct")]
LIVE = [("Masters Santiago", "19 Mar - 27 Mar", "#8a2be2"), ("VCL Korea", "19 Mar - 27 Mar", "#17b890")]
UPCOMING = [("VCL China", "20 Mar - 05 Apr", "#17b890"), ("CN Stage 1", "1 Apr", "#e0263b"),
            ("EMEA Stage 1", "1 Apr", "#b6e01b"), ("APAC Stage 1", "8 Apr", "#19b8e6"),
            ("AMER Stage 1", "11 Apr", "#f07a1d")]
TEAM_COLORS = {"BLG": "#2f6fe0", "TL": "#17358a", "RRQ": "#e8801f", "T1": "#d4202f", "C9": "#2aa6e0",
               "PRX": "#c01b2e", "VIT": "#f2c200", "NRG": "#e4402a", "WOL": "#f0a000", "EDG": "#6b7078",
               "FPX": "#c0222b", "AG": "#d8203c", "VKS": "#3a3f46", "GEN": "#c79a2b"}
TEAMS = {"None", *TEAM_COLORS}


# ------------------------------------------------------------------ pembatas percobaan
class RateLimiter:
    """Batas percobaan gagal dalam jendela waktu (dalam memori, per proses)."""

    def __init__(self, limit: int, window: int):
        self.limit, self.window = limit, window
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> deque:
        q = self._hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if not q:
            self._hits.pop(key, None)
            return deque()
        return q

    def wait(self, key: str) -> int:
        now = time.time()
        with self._lock:
            q = self._prune(key, now)
            return int(self.window - (now - q[0])) + 1 if len(q) >= self.limit else 0

    def hit(self, key: str) -> None:
        now = time.time()
        with self._lock:
            if len(self._hits) > 20000:
                for k in list(self._hits):
                    self._prune(k, now)
            self._hits[key].append(now)

    def reset(self, key: str) -> None:
        with self._lock:
            self._hits.pop(key, None)


LOGIN_USER = RateLimiter(5, 15 * 60)
LOGIN_IP = RateLimiter(20, 15 * 60)
REGISTER_IP = RateLimiter(10, 60 * 60)
PASSWORD_FAIL = RateLimiter(5, 15 * 60)


def client_ip() -> str:
    return request.remote_addr or "?"


def minutes(seconds: int) -> int:
    return max(1, math.ceil(seconds / 60))


# ------------------------------------------------------------------ util
def get_store() -> UserStore:
    return UserStore(USERS_FILE)


def get_msgs() -> MessageStore:
    return MessageStore(MESSAGES_FILE)


def get_forum() -> ForumStore:
    return ForumStore(FORUM_FILE)


def get_pickem() -> PickemStore:
    return PickemStore(PICKEM_FILE)


def get_chat() -> LiveChatStore:
    return LiveChatStore(CHAT_FILE)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            flash("Silakan login terlebih dahulu untuk mengakses halaman ini.", "warn")
            return redirect(url_for("login", next=request.full_path.rstrip("?")))
        return f(*args, **kwargs)
    return decorated_function


def get_user_fingerprint(user_data: dict) -> str:
    raw = f"{user_data.get('username', '')}:{user_data.get('hash', '')}:{user_data.get('salt', '')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def refresh_session_sig() -> None:
    rec = get_store().users.get(session.get("user", "").lower())
    if rec:
        session["user_sig"] = get_user_fingerprint(rec)


def csrf_token() -> str:
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


def force_terminate_session(reason: str, message: str, category: str = "error"):
    session.clear()
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "valid": False, "reason": reason, "message": message}), 401
    flash(message, category)
    return redirect(url_for("login"))


# ------------------------------------------------------------------ hook request
@app.before_request
def check_active_account_and_timeout():
    if request.endpoint == "static":
        return
    current_user = session.get("user")
    if not current_user:
        return
    now = time.time()
    last_active, login_at = session.get("last_active"), session.get("login_at")

    if session.get("boot_id") != SERVER_BOOT_ID or last_active is None or login_at is None:
        return force_terminate_session("invalid_session", "Sesi diperbarui oleh sistem. Silakan login kembali.", "warn")

    record = get_store().users.get(current_user.lower())
    if not record:
        return force_terminate_session("deleted", "Akun Anda sudah tidak aktif atau telah dihapus.", "error")
    if session.get("user_sig") != get_user_fingerprint(record):
        return force_terminate_session("credentials_changed", "Kredensial akun telah berubah. Silakan login ulang.", "warn")
    if now - last_active > IDLE_TIMEOUT_SECONDS:
        return force_terminate_session("timeout", "Sesi Anda berakhir karena tidak ada aktivitas (Idle Timeout).", "warn")
    if now - login_at > ABSOLUTE_TIMEOUT_SECONDS:
        return force_terminate_session("absolute_timeout", "Batas waktu sesi maksimal telah tercapai. Silakan login kembali.", "warn")

    if request.path != "/api/session-check":
        session["last_active"] = now
        session.modified = True


@app.before_request
def csrf_protect():
    if request.method in ("GET", "HEAD", "OPTIONS") or request.endpoint == "static":
        return
    sent = (request.form.get("csrf_token") or request.headers.get("X-CSRF-Token") or "").encode()
    good = (session.get("csrf") or "").encode()
    if good and hmac.compare_digest(sent, good):
        return
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "message": "Token keamanan tidak valid. Muat ulang halaman."}), 403
    if request.endpoint == "logout":
        session.clear()
        return redirect(url_for("login"))
    flash("Formulir kedaluwarsa. Silakan coba lagi.", "warn")
    return redirect(url_for("register" if request.endpoint == "register" else "login"))


@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; object-src 'none'; "
        "base-uri 'self'; form-action 'self'; frame-ancestors 'none'")
    if PROD:
        resp.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
    if request.endpoint != "static":
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
    return resp


@app.context_processor
def inject():
    return {"user": session.get("user"), "colors": TEAM_COLORS}


@app.errorhandler(StoreError)
def store_error(e):
    app.logger.error("StoreError: %s", e)
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "message": "Data sedang tidak dapat diakses. Coba lagi nanti."}), 503
    return "Layanan data sedang tidak tersedia. Coba lagi nanti.", 503


@app.errorhandler(413)
def too_large(e):
    return jsonify({"ok": False, "message": "Permintaan terlalu besar."}), 413


# ------------------------------------------------------------------ halaman
@app.route("/api/session-check")
def session_check():
    if not session.get("user"):
        return jsonify({"valid": False, "reason": "unauthenticated"}), 401
    return jsonify({"valid": True, "user": session["user"]})


@app.route("/")
def index():
    return redirect(url_for("home" if session.get("user") else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("home"))
    if request.method == "POST":
        u, p = request.form.get("username", "").strip()[:64], request.form.get("password", "")
        ip = client_ip()
        key = f"{ip}|{u.lower()}"
        wait = max(LOGIN_IP.wait(ip), LOGIN_USER.wait(key))
        if wait:
            flash(f"Terlalu banyak percobaan gagal. Coba lagi dalam {minutes(wait)} menit.", "error")
            return render_template("login.html"), 429
        if not u or not p:
            flash("Username dan password wajib diisi.", "warn")
        else:
            store = get_store()
            if store.authenticate(u, p):
                record = get_store().users.get(u.lower())
                if record is None:
                    flash("Username atau password salah.", "error")
                    return render_template("login.html")
                now = time.time()
                LOGIN_USER.reset(key)
                session.clear()
                session.permanent = True
                session["user"] = record["username"]
                session["boot_id"] = SERVER_BOOT_ID
                session["user_sig"] = get_user_fingerprint(record)
                session["login_at"] = now
                session["last_active"] = now
                return redirect(url_for("home"))
            LOGIN_IP.hit(ip)
            LOGIN_USER.hit(key)
            flash("Username atau password salah.", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user"):
        return redirect(url_for("home"))
    if request.method == "POST":
        ip = client_ip()
        wait = REGISTER_IP.wait(ip)
        if wait:
            flash(f"Terlalu banyak percobaan pendaftaran. Coba lagi dalam {minutes(wait)} menit.", "error")
            return render_template("register.html"), 429
        REGISTER_IP.hit(ip)
        f = request.form
        u, e = f.get("username", "").strip(), f.get("email", "").strip()
        p, c = f.get("password", ""), f.get("confirm", "")
        if not all((u, e, p, c)):
            flash("Semua kolom wajib diisi.", "warn")
        elif not USERNAME_RE.fullmatch(u):
            flash("Username 3-20 karakter: hanya huruf, angka, dan underscore.", "warn")
        elif not EMAIL_RE.fullmatch(e) or len(e) > 254:
            flash("Format email tidak valid.", "warn")
        elif not MIN_PASSWORD_LEN <= len(p) <= MAX_PASSWORD_LEN:
            flash(f"Password harus {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} karakter.", "warn")
        elif p != c:
            flash("Konfirmasi password tidak sama.", "warn")
        else:
            ok, msg = get_store().register(u, e, p)
            if ok:
                flash(msg + " Silakan login.", "ok")
                return redirect(url_for("login"))
            flash(msg, "error")
    return render_template("register.html")


@app.route("/home")
@login_required
def home():
    return render_template(
        "home.html",
        news=NEWS,
        news_slugs=NEWS_SLUG_MAP,
        matches=MATCHES,
        live=LIVE,
        upcoming=UPCOMING
    )


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# FEATURE ROUTES (IMK PROTOTYPES - ALL REQUIRE LOGIN)
# ============================================================
@app.route("/news/<slug>")
@login_required
def news_detail(slug):
    article = NEWS_ARTICLES.get(slug)
    if not article:
        flash("Artikel berita tidak ditemukan.", "warn")
        return redirect(url_for("home"))
    return render_template("news.html", article=article)


@app.route("/matches")
@login_required
def matches():
    active_tab = request.args.get("tab", "upcoming").lower()
    return render_template(
        "matches.html",
        active_tab=active_tab,
        upcoming_matches=UPCOMING_MATCHES_LIST,
        result_matches=RESULT_MATCHES_LIST
    )


@app.route("/match/<match_id>")
@login_required
def match_detail(match_id):
    match_data = DETAILED_MATCH_T1_PRX
    return render_template("match_detail.html", match=match_data)


@app.route("/watch")
@login_required
def watch():
    match_id = request.args.get("id", "").strip()
    watch_data = get_watch_match(match_id)
    room_id = watch_data.get("id") or LIVE_WATCH_MATCH["id"]
    chat_messages = get_chat().get_messages(match_id=room_id)
    return render_template("watch.html", watch_data=watch_data, chat_messages=chat_messages)


@app.route("/stats")
@login_required
def stats():
    event_series = request.args.get("event_series", "").strip()
    region = request.args.get("region", "").strip()
    min_rnds = request.args.get("min_rnds", "").strip()
    min_rating = request.args.get("min_rating", "").strip()
    agent = request.args.get("agent", "").strip()
    map_choice = request.args.get("map", "All").strip()
    timespan = request.args.get("timespan", "Past 60 Days").strip()

    players = list(STATS_PLAYERS_DATA)
    applied = False

    if min_rnds and min_rnds.isdigit():
        players = [p for p in players if p["rnd"] >= int(min_rnds)]
        applied = True
    if min_rating:
        try:
            m_rat = float(min_rating)
            players = [p for p in players if p["rating"] >= m_rat]
            applied = True
        except ValueError:
            pass
    if agent and agent.lower() != "all":
        players = [p for p in players if any(agent.lower() in a.lower() for a in p["agents"])]
        applied = True

    filters = {
        "event_series": event_series,
        "region": region,
        "min_rnds": min_rnds,
        "min_rating": min_rating,
        "agent": agent,
        "map": map_choice,
        "timespan": timespan,
        "applied": applied
    }
    return render_template("stats.html", players=players, filters=filters)


@app.route("/tournament/masters-santiago")
@app.route("/tournament/master-santiago")
@login_required
def tournament_santiago():
    sec = request.args.get("section", "overview").lower()
    sub = request.args.get("sub", "playoffs").lower()
    return render_template(
        "tournament.html",
        tourney=MASTER_SANTIAGO_DATA,
        active_section=sec,
        active_sub=sub
    )


@app.route("/tournament/cn-stage-1")
@login_required
def tournament_cn():
    return render_template("tournament_cn.html")


@app.route("/api/pickem/save", methods=["POST"])
@login_required
def api_save_pickem():
    user = session.get("user") or "Guest"
    picks = body()
    if not picks or len(picks) > 20 or not all(
        isinstance(k, str) and isinstance(v, str) and len(v) <= 50 for k, v in picks.items()
    ):
        return jsonify({"ok": False, "message": "Data Pick'em tidak valid."}), 400
    get_pickem().save_user_pickem(user, picks)
    return jsonify({"ok": True, "message": "Pick'em berhasil disimpan!"})


@app.route("/forum")
@login_required
def forum():
    q = request.args.get("q", "").strip()
    threads = get_forum().get_all(q)
    return render_template("forum.html", threads=threads, search_query=q)


@app.route("/forum/<thread_id>")
@login_required
def forum_thread(thread_id):
    t = get_forum().get_thread(thread_id)
    if not t:
        flash("Thread diskusi tidak ditemukan.", "warn")
        return redirect(url_for("forum"))
    return render_template("forum_thread.html", thread=t)


@app.route("/forum/new", methods=["GET", "POST"])
@login_required
def forum_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = session.get("user") or "Guest"
        if not title or not content:
            flash("Judul dan isi tulisan wajib diisi.", "warn")
        else:
            new_t = get_forum().create_thread(title, content, author)
            flash("Thread diskusi berhasil dipublikasikan!", "ok")
            return redirect(url_for("forum_thread", thread_id=new_t["id"]))
    return render_template("forum_new.html")


@app.route("/forum/<thread_id>/reply", methods=["POST"])
@login_required
def forum_reply(thread_id):
    comment = request.form.get("comment", "").strip()
    author = session.get("user") or "Guest"
    if not comment:
        flash("Komentar tidak boleh kosong.", "warn")
    elif get_forum().add_comment(thread_id, author, comment):
        flash("Balasan berhasil dikirim.", "ok")
    else:
        flash("Thread diskusi tidak ditemukan.", "error")
        return redirect(url_for("forum"))
    return redirect(url_for("forum_thread", thread_id=thread_id))


@app.route("/team/prx")
@app.route("/team/paper-rex")
@login_required
def team_prx():
    return render_template("team.html", team=TEAM_PAPER_REX)


@app.route("/player/f0rsaken")
@login_required
def player_f0rsaken():
    return render_template("player.html", player=PLAYER_F0RSAKEN)


@app.route("/search")
@login_required
def search():
    q = request.args.get("q", "").strip()
    results = []
    suggestion = None

    if q:
        q_clean = q.lower()
        if "prx" in q_clean or "paper" in q_clean or "rex" in q_clean:
            results.append({
                "title": "Paper Rex",
                "code": "PRX",
                "url": url_for("team_prx"),
                "description": "Tim esports profesional VCT Pacific, berbasis di Singapura."
            })
            results.append({
                "title": "f0rsakeN (Jason Susanto)",
                "code": "ID",
                "url": url_for("player_f0rsaken"),
                "description": "Pro player fleksibel Paper Rex asal Indonesia."
            })
        elif "santiago" in q_clean or "master" in q_clean:
            results.append({
                "title": "Master Santiago 2026",
                "code": "MS",
                "url": url_for("tournament_santiago"),
                "description": "Turnamen internasional VCT Masters Santiago 2026."
            })
        elif "china" in q_clean or "cn" in q_clean:
            results.append({
                "title": "VCT China Stage 1",
                "code": "CN",
                "url": url_for("tournament_cn"),
                "description": "Turnamen regional VCT China Stage 1 2026."
            })
        elif "tenz" in q_clean:
            results.append({
                "title": "TenZ Retirement",
                "code": "NEWS",
                "url": url_for("news_detail", slug="tenz-retirement"),
                "description": "Berita pengumuman masa pensiun Tyson 'TenZ' Ngo."
            })
        elif "carlotta" in q_clean or "fnatic" in q_clean:
            results.append({
                "title": "Carlotta Sign With FNATIC",
                "code": "NEWS",
                "url": url_for("news_detail", slug="carlotta-sign-with-fnatic"),
                "description": "Pengumuman rekrutan pemain baru FNATIC Carlotta."
            })
        else:
            if any(term in q_clean for term in ["pe er", "peerek", "perx", "pprx", "pe er eks", "perek"]):
                suggestion = "Paper Rex"

    return render_template("search.html", query=q, results=results, suggestion=suggestion)


# ------------------------------------------------------------------ API (wajib login + CSRF)
def api_user():
    user = session.get("user")
    if not user:
        return None, (jsonify({"ok": False, "message": "Belum login."}), 401)
    return user, None


def body() -> dict:
    d = request.get_json(silent=True)
    return d if isinstance(d, dict) else {}


def text(d: dict, k: str, default: str = "") -> str:
    v = d.get(k, default)
    return v if isinstance(v, str) else default


@app.route("/api/profile", methods=["GET"])
def api_profile():
    user, err = api_user()
    if err:
        return err
    prof = get_store().get_user(user)
    if not prof:
        return jsonify({"ok": False, "message": "Akun tidak ditemukan."}), 404
    return jsonify({"ok": True, **prof})


def _check_password(user: str, pwd: str):
    key = f"{client_ip()}|{user.lower()}"
    wait = PASSWORD_FAIL.wait(key)
    if wait:
        return False, (jsonify({"ok": False, "message": f"Terlalu banyak percobaan. Coba lagi dalam {minutes(wait)} menit."}), 429)
    if not get_store().authenticate(user, pwd):
        PASSWORD_FAIL.hit(key)
        return False, (jsonify({"ok": False, "message": "Password salah."}), 403)
    PASSWORD_FAIL.reset(key)
    refresh_session_sig()
    return True, None


@app.route("/api/profile/update", methods=["POST"])
def api_profile_update():
    user, err = api_user()
    if err:
        return err
    d = body()
    email, team, pwd = text(d, "email").strip(), text(d, "favorite_team", "None"), text(d, "password")
    if not pwd:
        return jsonify({"ok": False, "message": "Masukkan password Anda untuk konfirmasi perubahan."}), 400
    if team not in TEAMS:
        return jsonify({"ok": False, "message": "Tim favorit tidak valid."}), 400
    ok, err = _check_password(user, pwd)
    if not ok:
        return err
    ok, msg = get_store().update_profile(user, email, team)
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 400)


@app.route("/api/profile/password", methods=["POST"])
def api_profile_password():
    user, err = api_user()
    if err:
        return err
    d = body()
    old, new, conf = text(d, "old"), text(d, "new"), text(d, "confirm")
    if not (old and new and conf):
        return jsonify({"ok": False, "message": "Semua kolom wajib diisi."}), 400
    if not MIN_PASSWORD_LEN <= len(new) <= MAX_PASSWORD_LEN:
        return jsonify({"ok": False, "message": f"Password baru harus {MIN_PASSWORD_LEN}-{MAX_PASSWORD_LEN} karakter."}), 400
    if new != conf:
        return jsonify({"ok": False, "message": "Konfirmasi password baru tidak sama."}), 400
    ok, err = _check_password(user, old)
    if not ok:
        return err
    ok, msg = get_store().change_password(user, old, new)
    if ok:
        refresh_session_sig()
    return jsonify({"ok": ok, "message": msg}), (200 if ok else 400)


@app.route("/api/messages", methods=["GET"])
def api_messages():
    user, err = api_user()
    if err:
        return err
    msgs = get_msgs().get_messages(user)
    return jsonify({"ok": True, "messages": msgs, "unread": sum(1 for m in msgs if not m.get("read"))})


@app.route("/api/messages/read-all", methods=["POST"])
def api_messages_read_all():
    user, err = api_user()
    if err:
        return err
    get_msgs().mark_all_as_read(user)
    return jsonify({"ok": True})


@app.route("/api/messages/<msg_id>/read", methods=["POST"])
def api_message_read(msg_id):
    user, err = api_user()
    if err:
        return err
    read = body().get("read", True)
    ok = get_msgs().set_read(user, msg_id, bool(read))
    return jsonify({"ok": ok, "message": "" if ok else "Pesan tidak ditemukan."}), (200 if ok else 404)


@app.route("/api/messages/<msg_id>", methods=["DELETE"])
def api_message_delete(msg_id):
    user, err = api_user()
    if err:
        return err
    ok = get_msgs().delete_message(user, msg_id)
    return jsonify({"ok": ok, "message": "" if ok else "Pesan tidak ditemukan."}), (200 if ok else 404)


@app.route("/api/chat/messages", methods=["GET"])
def api_chat_messages():
    user, err = api_user()
    if err:
        return err
    match_id = request.args.get("match_id", "").strip() or None
    since_id = request.args.get("since", "").strip() or None
    msgs = get_chat().get_messages(match_id=match_id, since_id=since_id)
    return jsonify({"ok": True, "messages": msgs})


@app.route("/api/chat/send", methods=["POST"])
def api_chat_send():
    user, err = api_user()
    if err:
        return err
    d = body()
    match_id = text(d, "match_id").strip() or None
    msg_text = text(d, "msg").strip()
    if not msg_text:
        return jsonify({"ok": False, "message": "Pesan tidak boleh kosong."}), 400
    if len(msg_text) > 300:
        return jsonify({"ok": False, "message": "Pesan maksimal 300 karakter."}), 400
    try:
        new_msg = get_chat().add_message(sender=user, msg=msg_text, match_id=match_id)
        return jsonify({"ok": True, "message": new_msg})
    except Exception:
        return jsonify({"ok": False, "message": "Gagal menyimpan pesan."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=os.environ.get("FLASK_DEBUG") == "1")
