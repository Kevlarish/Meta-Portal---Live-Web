"""
portal_data.py - Data store dan dataset lengkap untuk META.PORTAL
Mencakup data matches, tournaments, pick'ems, stats, teams, players, dan news
sesuai dengan prototype UI/UX mata kuliah IMK.
"""

from __future__ import annotations

# ============================================================
# 1. NEWS DATA (Articles & Feeds)
# ============================================================
NEWS_ARTICLES = {
    "carlotta-sign-with-fnatic": {
        "slug": "carlotta-sign-with-fnatic",
        "title": "Carlotta Sign With FNATIC",
        "author": "META Esports Desk",
        "date": "24 Oct 2026",
        "badge": "Breaking News",
        "summary": "In a surprise roster move, FNATIC has officially announced the signing of Carlotta to reinforce their Valorant lineup ahead of the upcoming international circuit.",
        "content": [
            "In a major announcement that has sent shockwaves through the competitive Valorant scene, FNATIC has confirmed the signing of Carlotta to their active roster for the upcoming season.",
            "Carlotta, known for exceptional flexibility and clutch decision-making in high-pressure situations, joins an already formidable squad looking to reclaim international dominance.",
            "'We are thrilled to welcome Carlotta to the black and orange family,' said the FNATIC coaching staff in an official briefing. 'Their mechanical skill and tactical understanding of the evolving meta make them an invaluable addition to our roster.'",
            "Fans can expect Carlotta to make their official debut with FNATIC in the opening matches of the VCT EMEA Stage 1."
        ]
    },
    "tenz-retirement": {
        "slug": "tenz-retirement",
        "title": "TenZ Retirement",
        "author": "META Esports Desk",
        "date": "22 Oct 2026",
        "badge": "Community",
        "summary": "Tyson 'TenZ' Ngo announces his retirement from competitive Valorant to focus fully on content creation and streaming.",
        "content": [
            "After years of dominating the server and redefining what it means to be a superstar in Valorant, Tyson \"TenZ\" Ngo has officially announced his retirement from competitive play. The Sentinels legend, who became the global face of the game during its early days, is hanging up his mouse to focus fully on streaming and content creation.",
            "TenZ's journey in Valorant is nothing short of iconic. From leading Sentinels to a flawless, map-undefeated victory at Masters Reykjavik in 2021, to his incredible redemption arc winning Masters Madrid in 2024, his mechanical brilliance and flashy plays have inspired millions of players worldwide.",
            "While fans will deeply miss seeing him compete on the main stage, TenZ expressed that he is at peace with his decision and ready for the next chapter of his life. He steps away not just as a two-time international champion, but as one of the most influential players in esports history. The competitive scene won't be the same without him, but his legacy in Valorant is permanently secured."
        ]
    },
    "drx-calls-up-yong": {
        "slug": "drx-calls-up-yong",
        "title": 'DRX Calls up academy teams player "yong" to main rosters',
        "author": "META Korea",
        "date": "20 Oct 2026",
        "badge": "Roster Move",
        "summary": "DRX continues their talent development philosophy by promoting academy prospect yong.",
        "content": [
            "Korean powerhouse DRX has once again looked within their renowned developmental pipeline, promoting academy sensation 'yong' to their active VCT Pacific roster.",
            "Yong impressed throughout the Challengers Korea split with stellar initiator play and unmatched utility usage. He is expected to start immediately in the upcoming Pacific Kickoff."
        ]
    },
    "m80-statement": {
        "slug": "m80-statement",
        "title": "M80 Statement",
        "author": "META Americas",
        "date": "19 Oct 2026",
        "badge": "Official",
        "summary": "M80 management addresses competitive integrity and outlines their roadmap for Ascension.",
        "content": [
            "North American organization M80 has released an official statement regarding their long-term commitment to Valorant Ascension and the path to VCT Americas.",
            "'We remain resolute in our pursuit of tier 1 excellence,' the organization noted. 'Our support for our players and staff has never wavered.'"
        ]
    },
    "nongshim-red-force-history": {
        "slug": "nongshim-red-force-history",
        "title": "Nongshim Red Force make a legendary history",
        "author": "META Korea",
        "date": "18 Oct 2026",
        "badge": "Tournament",
        "summary": "NS Red Force secures an unprecedented reverse sweep in the Korean playoffs.",
        "content": [
            "In one of the most electric grand finals in Challengers Korea history, Nongshim Red Force rallied back from a 0-2 deficit to complete a legendary reverse sweep, lifting the trophy before a roaring crowd."
        ]
    },
    "paper-rex-dominates-nrg": {
        "slug": "paper-rex-dominates-nrg",
        "title": "Paper Rex dominates NRG",
        "author": "META Global",
        "date": "17 Oct 2026",
        "badge": "Match Recap",
        "summary": "PRX's signature aggressive tempo leaves NRG stunned in a decisive 2-0 sweep.",
        "content": [
            "Pacific crowd favorites Paper Rex delivered a masterclass in relentless aggression, dismantling Americas giant NRG in straight maps (13-5 Lotus, 13-8 Sunset).",
            "Jinggg and f0rsakeN combined for 45 kills, controlling pace and denying NRG any opportunity to settle into their defensive setups."
        ]
    },
    "funplusphoenix-sign-sacy": {
        "slug": "funplusphoenix-sign-sacy",
        "title": 'FunPlusPhoenix sign "Sacy" to the squad',
        "author": "META China",
        "date": "16 Oct 2026",
        "badge": "Roster Move",
        "summary": "World champion initiator Sacy brings his veteran leadership to FPX.",
        "content": [
            "FunPlusPhoenix has stunned international observers by announcing the acquisition of Brazilian world champion Gustavo 'Sacy' Rossi as an in-game leader and veteran anchor."
        ]
    }
}


# ============================================================
# 2. MATCHES DATA (Upcoming, Live, & Results)
# ============================================================
UPCOMING_MATCHES_LIST = [
    {
        "id": "m-up-1",
        "time": "14:00",
        "flag_a": "🇯🇵",
        "team_a": "REIGNITE FOXX",
        "team_a_code": "RGN",
        "team_a_tag": "#JP1",
        "score_a": "1",
        "flag_b": "🇯🇵",
        "team_b": "Insomnia",
        "team_b_code": "INS",
        "team_b_tag": "#JP2",
        "score_b": "1",
        "status_type": "live",
        "status_text": "LIVE",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Phase 2-Lower Round 1",
        "tournament_name": "Challengers 2026: Japan Split 1",
        "accent": "#17b890",
        "lineup_team_name": "REIGNITE FOXX LINEUP",
        "lineup_players": ["DHY", "RIPP", "Kuro", "Sora", "Nagi"]
    },
    {
        "id": "m-up-2",
        "time": "16:00",
        "flag_a": "🇨🇳",
        "team_a": "FunPlus Phoenix",
        "team_a_code": "FPX",
        "team_a_tag": "#CN1",
        "score_a": "0",
        "flag_b": "🇨🇳",
        "team_b": "TYLOO",
        "team_b_code": "TYL",
        "team_b_tag": "#CN2",
        "score_b": "1",
        "status_type": "live",
        "status_text": "LIVE",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Group Stage-Week 2",
        "tournament_name": "VCT 2026: China Stage 1",
        "accent": "#e0263b",
        "lineup_team_name": "FUNPLUS PHOENIX LINEUP",
        "lineup_players": ["AAAAY", "SACY", "BERLIN", "LIFE", "AUTUMN"]
    },
    {
        "id": "m-up-3",
        "time": "17:00",
        "flag_a": "🇯🇵",
        "team_a": "WEC C",
        "team_a_code": "WEC",
        "team_a_tag": "#JP3",
        "score_a": "0",
        "flag_b": "🇯🇵",
        "team_b": "RIDDLE ORDER",
        "team_b_code": "RDL",
        "team_b_tag": "#JP1",
        "score_b": "0",
        "status_type": "live",
        "status_text": "LIVE",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Phase 2-Lower Round 1",
        "tournament_name": "Challengers 2026: Japan Split 1",
        "accent": "#17b890",
        "lineup_team_name": "RIDDLE ORDER LINEUP",
        "lineup_players": ["CAEDYE", "SEOLDAM", "JOXJO", "AACE", "YATSUKA"]
    },
    {
        "id": "m-up-4",
        "time": "18:00",
        "flag_a": "🇨🇳",
        "team_a": "Titan Esports Club",
        "team_a_code": "TEC",
        "team_a_tag": "#CN4",
        "score_a": "-",
        "flag_b": "🇨🇳",
        "team_b": "Bilibili Gaming",
        "team_b_code": "BLG",
        "team_b_tag": "#CHINA1",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Group Stage-Week 2",
        "tournament_name": "VCT 2026: China Stage 1",
        "accent": "#e0263b",
        "lineup_team_name": "BILIBILI GAMING LINEUP",
        "lineup_players": ["WHZY", "NEPHH", "KNIGHT", "BIAN", "LEVIUS"]
    },
    {
        "id": "m-up-5",
        "time": "18:00",
        "flag_a": "🇸🇦",
        "team_a": "Team Falcons Vega",
        "team_a_code": "FLC",
        "team_a_tag": "#MENA1",
        "score_a": "-",
        "flag_b": "🇵🇭",
        "team_b": "TRENTITAS",
        "team_b_code": "TRN",
        "team_b_tag": "#SEA2",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Playoffs-Upper Quarterfinals",
        "tournament_name": "Game Changers 2026: Southeast Asia",
        "accent": "#f0a000",
        "lineup_team_name": "TEAM FALCONS VEGA LINEUP",
        "lineup_players": ["MARY", "MODI", "SANDRA", "NEV", "LUNA"]
    },
    {
        "id": "m-up-6",
        "time": "21:00",
        "flag_a": "🇲🇾",
        "team_a": "IVY",
        "team_a_code": "IVY",
        "team_a_tag": "#MY1",
        "score_a": "-",
        "flag_b": "🇦🇺",
        "team_b": "Azure GC",
        "team_b_code": "AZR",
        "team_b_tag": "#OCE1",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 3h 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Playoffs-Upper Quarterfinals",
        "tournament_name": "Game Changers 2026: Southeast Asia",
        "accent": "#f0a000",
        "lineup_team_name": "IVY TEAM LINEUP",
        "lineup_players": ["KAI", "LYNN", "HANA", "MIRA", "ZOE"]
    },
    {
        "id": "m-up-7",
        "time": "21:30",
        "flag_a": "🇹🇷",
        "team_a": "Fire Flux Esports",
        "team_a_code": "FF",
        "team_a_tag": "#TR1",
        "score_a": "-",
        "flag_b": "🇹🇷",
        "team_b": "REBORN",
        "team_b_code": "RBN",
        "team_b_tag": "#TR2",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 4h 19m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Group Stage-Week 1",
        "tournament_name": "Challengers 2026: Türkiye Birlik",
        "accent": "#f2c200",
        "lineup_team_name": "FIRE FLUX LINEUP",
        "lineup_players": ["LAU", "WO0T", "RUXIC", "SOCIABLEE", "QRAXS"]
    },
    {
        "id": "m-up-8",
        "time": "22:00",
        "flag_a": "🇪🇸",
        "team_a": "Barça eSports",
        "team_a_code": "BAR",
        "team_a_tag": "#ES1",
        "score_a": "-",
        "flag_b": "🇪🇸",
        "team_b": "Otakar Esports",
        "team_b_code": "OTK",
        "team_b_tag": "#ES2",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 4h 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Phase 1-Upper Semifinals",
        "tournament_name": "Challengers 2026: Spain Rising",
        "accent": "#f2c200",
        "lineup_team_name": "BARÇA ESPORTS LINEUP",
        "lineup_players": ["GUARD", "VORWEN", "FIT1NHO", "KILES", "MANIEK"]
    },
    {
        "id": "m-up-9",
        "time": "22:00",
        "flag_a": "🇮🇹",
        "team_a": "NOVO Esports",
        "team_a_code": "NOV",
        "team_a_tag": "#IT1",
        "score_a": "-",
        "flag_b": "🇮🇹",
        "team_b": "HGE Esport",
        "team_b_code": "HGE",
        "team_b_tag": "#IT2",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 4h 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Phase 1-Lower Round 1",
        "tournament_name": "Challengers 2026: Spain Rising",
        "accent": "#f2c200",
        "lineup_team_name": "NOVO ESPORTS LINEUP",
        "lineup_players": ["ALORANTE", "BJOR", "SIMON", "REX", "VEX"]
    },
    {
        "id": "m-up-10",
        "time": "23:00",
        "flag_a": "🇩🇪",
        "team_a": "RIZON",
        "team_a_code": "RZN",
        "team_a_tag": "#DACH1",
        "score_a": "-",
        "flag_b": "🇩🇪",
        "team_b": "CGN Esports",
        "team_b_code": "CGN",
        "team_b_tag": "#DACH2",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 5h 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Group Stage-Week 2",
        "tournament_name": "Challengers 2026: DACH Evolution",
        "accent": "#e0263b",
        "lineup_team_name": "CGN ESPORTS LINEUP",
        "lineup_players": ["BENNYY", "AZURY", "DAVI", "ELIAS", "KAI"]
    },
    {
        "id": "m-up-11",
        "time": "23:00",
        "flag_a": "🇩🇪",
        "team_a": "AKA HERO",
        "team_a_code": "AKA",
        "team_a_tag": "#DACH3",
        "score_a": "-",
        "flag_b": "🇩🇪",
        "team_b": "FOKUS",
        "team_b_code": "FKS",
        "team_b_tag": "#DACH1",
        "score_b": "-",
        "status_type": "upcoming",
        "status_text": "Upcoming 5h 49m",
        "stats_status": "Pending",
        "vods_status": "Pending",
        "tournament_stage": "Group Stage-Week 2",
        "tournament_name": "Challengers 2026: DACH Evolution",
        "accent": "#e0263b",
        "lineup_team_name": "FOKUS LINEUP",
        "lineup_players": ["JUGI", "YAABOY", "LUCA", "HOOD", "MOE"]
    }
]

RESULT_MATCHES_LIST = [
    {
        "id": "m-res-1",
        "time": "06:10",
        "flag_a": "🇺🇸",
        "team_a": "Shopify Rebellion Black",
        "team_a_code": "SRB",
        "team_a_tag": "#NA1",
        "score_a": 2,
        "flag_b": "🇺🇸",
        "team_b": "QoR",
        "team_b_code": "QOR",
        "team_b_tag": "#NA2",
        "score_b": 0,
        "elapsed": "11h 30m",
        "has_stats": True,
        "tournament_stage": "Swiss Stage-Round 4 (2-1)",
        "tournament_name": "Challengers 2026: North America",
        "accent": "#17b890"
    },
    {
        "id": "m-res-2",
        "time": "06:00",
        "flag_a": "🇧🇷",
        "team_a": "Paysandu Esports",
        "team_a_code": "PAY",
        "team_a_tag": "#BR1",
        "score_a": 2,
        "flag_b": "🇧🇷",
        "team_b": "MIBR GC",
        "team_b_code": "MIBR",
        "team_b_tag": "#BR2",
        "score_b": 0,
        "elapsed": "11h 40m",
        "has_stats": True,
        "tournament_stage": "Access Series-Upper Semifinals",
        "tournament_name": "Challengers 2026: Brazil Gamers",
        "accent": "#17b890"
    },
    {
        "id": "m-res-3",
        "time": "06:00",
        "flag_a": "🇧🇷",
        "team_a": "Remo Esports",
        "team_a_code": "REM",
        "team_a_tag": "#BR3",
        "score_a": 1,
        "flag_b": "🇧🇷",
        "team_b": "Team Liquid Brazil",
        "team_b_code": "TLB",
        "team_b_tag": "#BR1",
        "score_b": 2,
        "elapsed": "11h 40m",
        "has_stats": True,
        "tournament_stage": "Access Series-Upper Semifinals",
        "tournament_name": "Challengers 2026: Brazil Gamers",
        "accent": "#17b890"
    },
    {
        "id": "m-res-4",
        "time": "05:20",
        "flag_a": "🇺🇸",
        "team_a": "Nightblood Gaming",
        "team_a_code": "NBG",
        "team_a_tag": "#NA3",
        "score_a": 2,
        "flag_b": "🇺🇸",
        "team_b": "Pigeons",
        "team_b_code": "PGN",
        "team_b_tag": "#NA4",
        "score_b": 1,
        "elapsed": "12h 20m",
        "has_stats": True,
        "tournament_stage": "Swiss Stage-Round 4 (1-2)",
        "tournament_name": "Challengers 2026: North America",
        "accent": "#17b890"
    },
    {
        "id": "m-res-5",
        "time": "03:00",
        "flag_a": "🇨🇦",
        "team_a": "Shopify Rebellion Gold",
        "team_a_code": "SRG",
        "team_a_tag": "#NA2",
        "score_a": 1,
        "flag_b": "🇺🇸",
        "team_b": "ROSE",
        "team_b_code": "ROSE",
        "team_b_tag": "#NA5",
        "score_b": 2,
        "elapsed": "14h 40m",
        "has_stats": True,
        "tournament_stage": "Swiss Stage-Round 4 (0-3)",
        "tournament_name": "Challengers 2026: North America",
        "accent": "#17b890"
    },
    {
        "id": "m-res-6",
        "time": "03:00",
        "flag_a": "🇺🇸",
        "team_a": "Evil Geniuses Academy",
        "team_a_code": "EGA",
        "team_a_tag": "#NA3",
        "score_a": 2,
        "flag_b": "🇺🇸",
        "team_b": "Division One",
        "team_b_code": "DIV1",
        "team_b_tag": "#NA6",
        "score_b": 0,
        "elapsed": "14h 40m",
        "has_stats": True,
        "tournament_stage": "Swiss Stage-Round 4 (1-2)",
        "tournament_name": "Challengers 2026: North America",
        "accent": "#17b890"
    },
    {
        "id": "m-res-7",
        "time": "03:00",
        "flag_a": "🇧🇷",
        "team_a": "MIBR GC",
        "team_a_code": "MIBR",
        "team_a_tag": "#BR2",
        "score_a": 2,
        "flag_b": "🇧🇷",
        "team_b": "Lost Puppies Quackers",
        "team_b_code": "LPQ",
        "team_b_tag": "#BR4",
        "score_b": 1,
        "elapsed": "14h 40m",
        "has_stats": True,
        "tournament_stage": "Access Series-Round of 6",
        "tournament_name": "Challengers 2026: Brazil Gamers",
        "accent": "#17b890"
    },
    {
        "id": "m-res-8",
        "time": "03:00",
        "flag_a": "🇧🇷",
        "team_a": "Team Liquid Brazil",
        "team_a_code": "TLB",
        "team_a_tag": "#BR1",
        "score_a": 2,
        "flag_b": "🇧🇷",
        "team_b": "Underhounds",
        "team_b_code": "UND",
        "team_b_tag": "#BR5",
        "score_b": 0,
        "elapsed": "14h 40m",
        "has_stats": True,
        "tournament_stage": "Access Series-Round of 6",
        "tournament_name": "Challengers 2026: Brazil Gamers",
        "accent": "#17b890"
    },
    {
        "id": "m-res-9",
        "time": "02:00",
        "flag_a": "🇦🇷",
        "team_a": "Olimpo Gold",
        "team_a_code": "OLM",
        "team_a_tag": "#LATAM2",
        "score_a": 0,
        "flag_b": "🇨🇱",
        "team_b": "KRÜ BLAZE",
        "team_b_code": "KRU",
        "team_b_tag": "#LATAM1",
        "score_b": 3,
        "elapsed": "15h 40m",
        "has_stats": True,
        "tournament_stage": "Playoffs-Grand Final",
        "tournament_name": "Game Changers 2026: LATAM",
        "accent": "#f0a000"
    },
    {
        "id": "m-res-10",
        "time": "01:35",
        "flag_a": "🇫🇷",
        "team_a": "Nuxeria Esport",
        "team_a_code": "NUX",
        "team_a_tag": "#FR1",
        "score_a": 2,
        "flag_b": "🇫🇷",
        "team_b": "F9 EICAR",
        "team_b_code": "F9",
        "team_b_tag": "#FR2",
        "score_b": 0,
        "elapsed": "16h 5m",
        "has_stats": True,
        "tournament_stage": "Group Stage-Week 1",
        "tournament_name": "Challengers 2026: France Revolution",
        "accent": "#f2c200"
    },
    {
        "id": "m-res-11",
        "time": "00:30",
        "flag_a": "🇮🇹",
        "team_a": "DNSTY",
        "team_a_code": "DNS",
        "team_a_tag": "#IT1",
        "score_a": 2,
        "flag_b": "🇪🇸",
        "team_b": "Ramboot Club",
        "team_b_code": "RBT",
        "team_b_tag": "#ES3",
        "score_b": 1,
        "elapsed": "17h 10m",
        "has_stats": True,
        "tournament_stage": "Phase 1-Upper Quarterfinals",
        "tournament_name": "Challengers 2026: Spain Rising",
        "accent": "#f2c200"
    }
]


# ============================================================
# 3. DETAILED MATCH BREAKDOWN (T1 vs PRX - Masters Santiago)
# ============================================================
DETAILED_MATCH_T1_PRX = {
    "id": "t1-vs-prx",
    "event": "Master Santiago 2026",
    "stage": "Swiss Round 2",
    "datetime": "12 March 16:00 WIB",
    "team_a": {
        "code": "T1",
        "name": "T1",
        "score": 1,
        "logo_color": "#d4202f"
    },
    "team_b": {
        "code": "PRX",
        "name": "Paper Rex",
        "score": 2,
        "logo_color": "#c01b2e"
    },
    "format": "Bo3",
    "streams": [
        {"platform": "YouTube", "channel": "VALORANT Champions Tour", "url": "https://youtube.com"},
        {"platform": "TikTok", "channel": "VALORANT Champions Tour", "url": "https://tiktok.com"},
        {"platform": "Twitch", "channel": "VALORANT Champions Tour", "url": "https://twitch.tv"},
    ],
    "vods": [
        {"map": "Map 1 - Lotus", "url": "#"},
        {"map": "Map 2 - Sunset", "url": "#"},
        {"map": "Map 3 - Bind", "url": "#"},
    ],
    "maps": ["All", "Lotus", "Sunset", "Bind"],
    "player_stats": {
        "All": {
            "prx": [
                {"name": "something", "flag": "🇷🇺", "team": "PRX", "r": 1.24, "acs": 252, "k": 61, "d": 45, "a": 12, "diff": "+16", "hs": "30%", "fk": 15, "fd": 7, "fk_diff": "+6"},
                {"name": "f0rsakeN", "flag": "🇮🇩", "team": "PRX", "r": 1.13, "acs": 222, "k": 54, "d": 47, "a": 26, "diff": "+7", "hs": "24%", "fk": 8, "fd": 6, "fk_diff": "+2"},
                {"name": "Jinggg", "flag": "🇸🇬", "team": "PRX", "r": 1.13, "acs": 233, "k": 58, "d": 51, "a": 12, "diff": "+7", "hs": "28%", "fk": 12, "fd": 10, "fk_diff": "+2"},
                {"name": "d4v41", "flag": "🇲🇾", "team": "PRX", "r": 1.05, "acs": 183, "k": 44, "d": 41, "a": 34, "diff": "+3", "hs": "21%", "fk": 3, "fd": 2, "fk_diff": "+1"},
                {"name": "invy", "flag": "🇵🇭", "team": "PRX", "r": 0.98, "acs": 162, "k": 37, "d": 40, "a": 31, "diff": "-3", "hs": "19%", "fk": 2, "fd": 2, "fk_diff": "0"},
            ],
            "t1": [
                {"name": "BuZz", "flag": "🇰🇷", "team": "T1", "r": 1.16, "acs": 238, "k": 59, "d": 51, "a": 12, "diff": "+8", "hs": "29%", "fk": 13, "fd": 11, "fk_diff": "+2"},
                {"name": "Munchkin", "flag": "🇰🇷", "team": "T1", "r": 0.97, "acs": 197, "k": 46, "d": 46, "a": 20, "diff": "0", "hs": "25%", "fk": 3, "fd": 5, "fk_diff": "-2"},
                {"name": "Meteor", "flag": "🇰🇷", "team": "T1", "r": 0.97, "acs": 193, "k": 45, "d": 50, "a": 14, "diff": "-5", "hs": "22%", "fk": 3, "fd": 6, "fk_diff": "-3"},
                {"name": "iZu", "flag": "🇰🇷", "team": "T1", "r": 0.93, "acs": 172, "k": 40, "d": 50, "a": 18, "diff": "-10", "hs": "21%", "fk": 5, "fd": 6, "fk_diff": "-1"},
                {"name": "Stax", "flag": "🇰🇷", "team": "T1", "r": 0.89, "acs": 163, "k": 38, "d": 51, "a": 28, "diff": "-13", "hs": "19%", "fk": 2, "fd": 5, "fk_diff": "-3"},
            ]
        },
        "Lotus": {
            "prx": [
                {"name": "something", "flag": "🇷🇺", "team": "PRX", "r": 1.35, "acs": 278, "k": 22, "d": 14, "a": 4, "diff": "+8", "hs": "32%", "fk": 6, "fd": 2, "fk_diff": "+4"},
                {"name": "f0rsakeN", "flag": "🇮🇩", "team": "PRX", "r": 1.20, "acs": 240, "k": 19, "d": 15, "a": 8, "diff": "+4", "hs": "26%", "fk": 3, "fd": 1, "fk_diff": "+2"},
                {"name": "Jinggg", "flag": "🇸🇬", "team": "PRX", "r": 1.15, "acs": 225, "k": 18, "d": 16, "a": 3, "diff": "+2", "hs": "25%", "fk": 4, "fd": 3, "fk_diff": "+1"},
                {"name": "d4v41", "flag": "🇲🇾", "team": "PRX", "r": 1.02, "acs": 175, "k": 14, "d": 13, "a": 11, "diff": "+1", "hs": "20%", "fk": 1, "fd": 0, "fk_diff": "+1"},
                {"name": "invy", "flag": "🇵🇭", "team": "PRX", "r": 0.95, "acs": 155, "k": 12, "d": 14, "a": 9, "diff": "-2", "hs": "18%", "fk": 1, "fd": 1, "fk_diff": "0"},
            ],
            "t1": [
                {"name": "BuZz", "flag": "🇰🇷", "team": "T1", "r": 1.10, "acs": 220, "k": 18, "d": 17, "a": 3, "diff": "+1", "hs": "28%", "fk": 4, "fd": 3, "fk_diff": "+1"},
                {"name": "Munchkin", "flag": "🇰🇷", "team": "T1", "r": 0.95, "acs": 185, "k": 15, "d": 16, "a": 6, "diff": "-1", "hs": "24%", "fk": 1, "fd": 2, "fk_diff": "-1"},
                {"name": "Meteor", "flag": "🇰🇷", "team": "T1", "r": 0.92, "acs": 178, "k": 14, "d": 17, "a": 4, "diff": "-3", "hs": "20%", "fk": 1, "fd": 2, "fk_diff": "-1"},
                {"name": "iZu", "flag": "🇰🇷", "team": "T1", "r": 0.90, "acs": 165, "k": 13, "d": 18, "a": 5, "diff": "-5", "hs": "19%", "fk": 1, "fd": 3, "fk_diff": "-2"},
                {"name": "Stax", "flag": "🇰🇷", "team": "T1", "r": 0.88, "acs": 150, "k": 12, "d": 17, "a": 9, "diff": "-5", "hs": "17%", "fk": 0, "fd": 2, "fk_diff": "-2"},
            ]
        }
    }
}


# ============================================================
# 4. LIVE WATCH ROOM (Default & Dynamic Lookup)
# ============================================================
LIVE_WATCH_MATCH = {
    "id": "blg-vs-tl",
    "title": "BiliBili vs Team Liquid - Upper Bracket Round 1",
    "video_title": "00:15:24 PLAYOFF DAY - 1",
    "status_type": "live",
    "status_text": "LIVE",
    "time": "16:00",
    "tournament_name": "Master Santiago 2026",
    "tournament_stage": "Upper Bracket Round 1",
    "flag_a": "🇨🇳",
    "team_a_name": "BiliBili Gaming",
    "team_a_code": "BLG",
    "team_a_tag": "#CHINA1",
    "score_a": "0",
    "flag_b": "🇪🇺",
    "team_b_name": "Team Liquid",
    "team_b_code": "TL",
    "team_b_tag": "#EMEA3",
    "score_b": "0",
    "secondary_game": {
        "team_a_code": "RRQ",
        "team_a_tag": "#PAC1",
        "team_b_code": "T1",
        "team_b_tag": "#PAC2",
    },
    "lineup_team_1": "BiliBili Gaming (BLG)",
    "lineup_team_2": "Team Liquid (TL)",
    "lineup_team_name": "T1 TEAM LINEUP",
    "lineup_players": ["CARPE", "IZU", "KDG", "METEOR", "MUNCHKIN"],
    "initial_chat": [
        {"sender": "Connor", "msg": "When does Sentinel plays?"},
        {"sender": "Ikuyo Kita", "msg": "Can't wait for BLG stomp TL"},
        {"sender": "Goldship", "msg": "hey guys"},
        {"sender": "Gigguk", "msg": "What's your pred goldship?"},
        {"sender": "Kazuma", "msg": "is it just us in here?"}
    ]
}


def get_watch_match(match_id: str | None) -> dict:
    """Cari data pertandingan untuk halaman /watch berdasarkan ID/slug; fallback ke LIVE_WATCH_MATCH."""
    if not match_id:
        return dict(LIVE_WATCH_MATCH)
    target = match_id.strip().lower()
    if target in ("", "default", LIVE_WATCH_MATCH["id"]):
        return dict(LIVE_WATCH_MATCH)

    for item in UPCOMING_MATCHES_LIST:
        if item["id"].lower() == target:
            is_live = item.get("status_type") == "live"
            video_title = (
                f"LIVE • {item['tournament_name'].upper()}"
                if is_live
                else f"{item['time']} WIB • {item['status_text'].upper()}"
            )
            return {
                "id": item["id"],
                "title": f"{item['team_a']} vs {item['team_b']} - {item['tournament_stage']}",
                "video_title": video_title,
                "status_type": item.get("status_type", "upcoming"),
                "status_text": item.get("status_text", "Upcoming"),
                "time": item.get("time", ""),
                "tournament_name": item.get("tournament_name", ""),
                "tournament_stage": item.get("tournament_stage", ""),
                "flag_a": item.get("flag_a", ""),
                "team_a_name": item["team_a"],
                "team_a_code": item.get("team_a_code", item["team_a"][:3].upper()),
                "team_a_tag": item.get("team_a_tag", "#TEAM1"),
                "score_a": item.get("score_a", "-"),
                "flag_b": item.get("flag_b", ""),
                "team_b_name": item["team_b"],
                "team_b_code": item.get("team_b_code", item["team_b"][:3].upper()),
                "team_b_tag": item.get("team_b_tag", "#TEAM2"),
                "score_b": item.get("score_b", "-"),
                "secondary_game": None,
                "lineup_team_1": f"{item['team_a']} ({item.get('team_a_code', '')})",
                "lineup_team_2": f"{item['team_b']} ({item.get('team_b_code', '')})",
                "lineup_team_name": item.get("lineup_team_name", f"{item['team_a'].upper()} LINEUP"),
                "lineup_players": item.get("lineup_players", ["PLAYER 1", "PLAYER 2", "PLAYER 3", "PLAYER 4", "PLAYER 5"]),
                "initial_chat": [],
            }

    for item in RESULT_MATCHES_LIST:
        if item["id"].lower() == target:
            return {
                "id": item["id"],
                "title": f"{item['team_a']} vs {item['team_b']} - {item['tournament_stage']}",
                "video_title": f"COMPLETED • {item['tournament_name'].upper()}",
                "status_type": "completed",
                "status_text": f"Completed {item.get('elapsed', '')}".strip(),
                "time": item.get("time", ""),
                "tournament_name": item.get("tournament_name", ""),
                "tournament_stage": item.get("tournament_stage", ""),
                "flag_a": item.get("flag_a", ""),
                "team_a_name": item["team_a"],
                "team_a_code": item.get("team_a_code", item["team_a"][:3].upper()),
                "team_a_tag": item.get("team_a_tag", "#TEAM1"),
                "score_a": str(item.get("score_a", 0)),
                "flag_b": item.get("flag_b", ""),
                "team_b_name": item["team_b"],
                "team_b_code": item.get("team_b_code", item["team_b"][:3].upper()),
                "team_b_tag": item.get("team_b_tag", "#TEAM2"),
                "score_b": str(item.get("score_b", 0)),
                "secondary_game": None,
                "lineup_team_1": f"{item['team_a']} ({item.get('team_a_code', '')})",
                "lineup_team_2": f"{item['team_b']} ({item.get('team_b_code', '')})",
                "lineup_team_name": f"{item['team_a'].upper()} LINEUP",
                "lineup_players": ["PLAYER 1", "PLAYER 2", "PLAYER 3", "PLAYER 4", "PLAYER 5"],
                "initial_chat": [],
            }

    return dict(LIVE_WATCH_MATCH)


# ============================================================
# 5. TOURNAMENT HUB: MASTER SANTIAGO 2026
# ============================================================
MASTER_SANTIAGO_DATA = {
    "name": "Master Santiago 2026",
    "dates": "10 March - 29 March 2026",
    "active_dates": "16-29 March",
    "swiss_stage": {
        "round_1": [
            ("LEV", "TE"), ("XLG", "PRX"), ("TL", "NRG"), ("T1", "BBL")
        ],
        "round_2_1_0": [("T1", "PRX"), ("TE", "TL")],
        "round_2_0_1": [("LEV", "NRG"), ("XLG", "BBL")],
        "round_3_1_1": [("T1", "TE"), ("BBL", "NRG")],
        "advances_to_playoff": ["PRX", "TL", "T1", "NRG"],
        "eliminated": ["XLG", "LEV", "TE", "BBL"],
        "prizes": [
            {"place": "9-10th", "prize": "$25.000", "team": "BBL Esports (Europe)"},
            {"place": "9-10th", "prize": "$25.000", "team": "Trace Esports (China)"},
            {"place": "11-12th", "prize": "$15.000", "team": "Leviatán (Americas)"},
            {"place": "11-12th", "prize": "$15.000", "team": "XLG Esports (China)"},
        ],
        "participating": [
            {"name": "Leviatán", "seed": "Americas Kickoff #2"},
            {"name": "NRG", "seed": "Americas Kickoff #3"},
            {"name": "Trace Esports", "seed": "China Kickoff #2"},
            {"name": "XLG Esports", "seed": "China Kickoff #3"},
            {"name": "Team Liquid", "seed": "EMEA Kickoff #2"},
            {"name": "BBL Esports", "seed": "EMEA Kickoff #3"},
            {"name": "T1", "seed": "Pacific Kickoff #2"},
            {"name": "Paper Rex", "seed": "Pacific Kickoff #3"},
        ]
    },
    "playoffs": {
        "prizes": [
            {"place": "1st", "prize": "$350.000", "points": "+6"},
            {"place": "2nd", "prize": "$200.000", "points": "+4"},
            {"place": "3rd", "prize": "$125.000", "points": "+3"},
            {"place": "4th", "prize": "$75.000", "points": "+2"},
            {"place": "5-6th", "prize": "$50.000", "points": "+1"},
            {"place": "5-6th", "prize": "$50.000", "points": "+1"},
            {"place": "7-8th", "prize": "$35.000", "points": ""},
            {"place": "7-8th", "prize": "$35.000", "points": ""},
        ],
        "participating": [
            {"code": "BLG", "name": "BiliBili Gaming", "seed": "China Kickoff #1", "bg": "#2f6fe0"},
            {"code": "C9", "name": "Cloud 9", "seed": "Americas Kickoff #1", "bg": "#2aa6e0"},
            {"code": "RRQ", "name": "Rex Regum Qeon", "seed": "Pacific Kickoff #1", "bg": "#e8801f"},
            {"code": "VIT", "name": "Team Vitality", "seed": "EMEA Kickoff #1", "bg": "#f2c200"},
            {"code": "TL", "name": "Team Liquid", "seed": "Swiss Stage 2-0", "bg": "#17358a"},
            {"code": "PRX", "name": "Paper Rex", "seed": "Swiss Stage 2-0", "bg": "#c01b2e"},
            {"code": "T1", "name": "T1", "seed": "Swiss Stage 2-1", "bg": "#d4202f"},
            {"code": "NRG", "name": "NRG", "seed": "Swiss Stage 2-1", "bg": "#e4402a"},
        ],
        "bracket_rounds": [
            {
                "name": "Upper Bracket Round 1",
                "matches": [
                    {"id": "ub-r1-1", "team1": "BiliBili Gaming", "team2": "Team Liquid"},
                    {"id": "ub-r1-2", "team1": "Cloud 9", "team2": "Paper Rex"},
                    {"id": "ub-r1-3", "team1": "Rex Regum Qeon", "team2": "T1"},
                    {"id": "ub-r1-4", "team1": "Team Vitality", "team2": "NRG"},
                ]
            },
            {
                "name": "Upper Bracket Round 2",
                "matches": [
                    {"id": "ub-r2-1", "team1": "TBD", "team2": "TBD"},
                    {"id": "ub-r2-2", "team1": "TBD", "team2": "TBD"},
                ]
            },
            {
                "name": "Upper Bracket Final",
                "matches": [
                    {"id": "ub-fn", "team1": "TBD", "team2": "TBD"},
                ]
            },
            {
                "name": "Grand Final",
                "matches": [
                    {"id": "gf", "team1": "TBD", "team2": "TBD"},
                ]
            }
        ]
    },
    "leaderboard": [
        {"rank": 1, "pts": 315, "flag": "🇺🇸", "user": "daffyduckwill", "country": "United States"},
        {"rank": 2, "pts": 305, "flag": "🇫🇷", "user": "Azzrod", "country": "France"},
        {"rank": 3, "pts": 300, "flag": "🇸🇱", "user": "MrBlooBloom", "country": "Sierra Leone"},
        {"rank": 4, "pts": 300, "flag": "🇵🇹", "user": "ruben6_", "country": "Portugal"},
        {"rank": 5, "pts": 295, "flag": "🇺🇸", "user": "ishoudaran", "country": "United States"},
        {"rank": 6, "pts": 295, "flag": "🇨🇦", "user": "princeeroni", "country": "Canada"},
        {"rank": 7, "pts": 290, "flag": "🇪🇺", "user": "SusCat04", "country": "Europe"},
        {"rank": 8, "pts": 290, "flag": "🇺🇸", "user": "Danpphy", "country": "United States"},
        {"rank": 9, "pts": 285, "flag": "🇨🇳", "user": "aurafarmer99", "country": "China"},
    ]
}


# ============================================================
# 6. STATS HUB DATA (Player Metrics & Tiers)
# ============================================================
STATS_PLAYERS_DATA = [
    {
        "player": "vo0kashu", "team": "DRG", "flag": "🇷🇺", "agents": ["Cypher", "Killjoy"],
        "rnd": 384, "rating": 1.27, "acs": 223.1, "kd": 1.24, "kast": "74%", "adr": 151.3,
        "kpr": 0.81, "apr": 0.26, "fkpr": 0.07, "fdpr": 0.06, "hs": "28%", "cl_pct": "-",
        "cl": "-", "kmax": 28, "k": 310, "d": 250, "a": 100, "fk": 27, "tier": "S"
    },
    {
        "player": "Neon", "team": "LEV", "flag": "🇦🇷", "agents": ["Jett", "Raze"],
        "rnd": 543, "rating": 1.25, "acs": 226.6, "kd": 1.45, "kast": "77%", "adr": 147.1,
        "kpr": 0.83, "apr": 0.27, "fkpr": 0.13, "fdpr": 0.09, "hs": "25%", "cl_pct": "15%",
        "cl": "11/72", "kmax": 25, "k": 448, "d": 309, "a": 145, "fk": 69, "tier": "S"
    },
    {
        "player": "nephh", "team": "BLG", "flag": "🇸🇬", "agents": ["KAY/O", "Breach"],
        "rnd": 208, "rating": 1.24, "acs": 224.1, "kd": 1.27, "kast": "76%", "adr": 135.4,
        "kpr": 0.81, "apr": 0.37, "fkpr": 0.07, "fdpr": 0.07, "hs": "23%", "cl_pct": "-",
        "cl": "-", "kmax": 23, "k": 169, "d": 133, "a": 77, "fk": 15, "tier": "S"
    },
    {
        "player": "brawk", "team": "NRG", "flag": "🇺🇸", "agents": ["Sova", "Fade"],
        "rnd": 446, "rating": 1.24, "acs": 226.3, "kd": 1.27, "kast": "78%", "adr": 147.3,
        "kpr": 0.77, "apr": 0.40, "fkpr": 0.07, "fdpr": 0.04, "hs": "18%", "cl_pct": "12%",
        "cl": "9/74", "kmax": 26, "k": 344, "d": 270, "a": 178, "fk": 31, "tier": "S"
    },
    {
        "player": "AAAAY", "team": "FPX", "flag": "🇨🇳", "agents": ["Gekko", "Skye"],
        "rnd": 224, "rating": 1.21, "acs": 241.6, "kd": 1.32, "kast": "79%", "adr": 154.3,
        "kpr": 0.88, "apr": 0.22, "fkpr": 0.11, "fdpr": 0.04, "hs": "38%", "cl_pct": "-",
        "cl": "-", "kmax": 29, "k": 196, "d": 148, "a": 50, "fk": 21, "tier": "A"
    },
    {
        "player": "primmie", "team": "FS", "flag": "🇹🇭", "agents": ["Reyna", "Jett"],
        "rnd": 403, "rating": 1.21, "acs": 263.2, "kd": 1.26, "kast": "73%", "adr": 164.7,
        "kpr": 0.91, "apr": 0.23, "fkpr": 0.19, "fdpr": 0.14, "hs": "30%", "cl_pct": "21%",
        "cl": "7/34", "kmax": 25, "k": 366, "d": 291, "a": 93, "fk": 78, "tier": "A"
    },
    {
        "player": "CHICHOO", "team": "EDG", "flag": "🇨🇳", "agents": ["Omen", "Astra"],
        "rnd": 435, "rating": 1.21, "acs": 218.7, "kd": 1.27, "kast": "77%", "adr": 142.2,
        "kpr": 0.79, "apr": 0.32, "fkpr": 0.07, "fdpr": 0.08, "hs": "29%", "cl_pct": "-",
        "cl": "-", "kmax": 23, "k": 343, "d": 271, "a": 139, "fk": 32, "tier": "A"
    },
    {
        "player": "something", "team": "PRX", "flag": "🇷🇺", "agents": ["Jett", "Reyna"],
        "rnd": 513, "rating": 1.21, "acs": 237.0, "kd": 1.39, "kast": "73%", "adr": 153.6,
        "kpr": 0.86, "apr": 0.17, "fkpr": 0.18, "fdpr": 0.11, "hs": "23%", "cl_pct": "15%",
        "cl": "8/52", "kmax": 28, "k": 443, "d": 319, "a": 88, "fk": 91, "tier": "A"
    },
    {
        "player": "slowly", "team": "TYL", "flag": "🇨🇳", "agents": ["Iso", "Yoru"],
        "rnd": 404, "rating": 1.20, "acs": 217.5, "kd": 1.22, "kast": "73%", "adr": 144.2,
        "kpr": 0.79, "apr": 0.32, "fkpr": 0.06, "fdpr": 0.06, "hs": "30%", "cl_pct": "-",
        "cl": "-", "kmax": 28, "k": 321, "d": 263, "a": 128, "fk": 22, "tier": "A"
    },
    {
        "player": "Smoggy", "team": "EDG", "flag": "🇨🇳", "agents": ["Clove", "Viper"],
        "rnd": 435, "rating": 1.20, "acs": 227.9, "kd": 1.20, "kast": "78%", "adr": 149.6,
        "kpr": 0.80, "apr": 0.40, "fkpr": 0.12, "fdpr": 0.08, "hs": "26%", "cl_pct": "-",
        "cl": "-", "kmax": 26, "k": 348, "d": 290, "a": 172, "fk": 51, "tier": "B"
    },
    {
        "player": "Less", "team": "KRÜ", "flag": "🇧🇷", "agents": ["Viper", "Deadlock"],
        "rnd": 268, "rating": 1.18, "acs": 233.5, "kd": 1.29, "kast": "70%", "adr": 152.9,
        "kpr": 0.84, "apr": 0.24, "fkpr": 0.10, "fdpr": 0.10, "hs": "29%", "cl_pct": "10%",
        "cl": "4/42", "kmax": 27, "k": 224, "d": 173, "a": 65, "fk": 26, "tier": "B"
    },
    {
        "player": "Jinggg", "team": "PRX", "flag": "🇸🇬", "agents": ["Raze", "Phoenix"],
        "rnd": 513, "rating": 1.17, "acs": 236.1, "kd": 1.24, "kast": "77%", "adr": 154.5,
        "kpr": 0.83, "apr": 0.31, "fkpr": 0.13, "fdpr": 0.09, "hs": "26%", "cl_pct": "15%",
        "cl": "6/39", "kmax": 36, "k": 425, "d": 343, "a": 159, "fk": 66, "tier": "B"
    },
    {
        "player": "Meiy", "team": "DFM", "flag": "🇯🇵", "agents": ["Neon", "Jett"],
        "rnd": 296, "rating": 1.17, "acs": 249.7, "kd": 1.18, "kast": "73%", "adr": 154.8,
        "kpr": 0.89, "apr": 0.16, "fkpr": 0.21, "fdpr": 0.12, "hs": "28%", "cl_pct": "16%",
        "cl": "5/32", "kmax": 36, "k": 264, "d": 223, "a": 48, "fk": 62, "tier": "B"
    }
]


# ============================================================
# 7. TEAM & PLAYER PROFILES
# ============================================================
TEAM_PAPER_REX = {
    "code": "PRX",
    "name": "Paper Rex",
    "region": "Pacific",
    "roster": [
        {"name": "invy", "real_name": "Adrian Jiggs Reyes", "flag": "🇵🇭", "role": "Player"},
        {"name": "Jinggg", "real_name": "Wang Jing Jie", "flag": "🇸🇬", "role": "Player"},
        {"name": "f0rsakeN", "real_name": "Jason Susanto", "flag": "🇮🇩", "role": "Player"},
        {"name": "d4v41", "real_name": "Khalish Rusyaidee", "flag": "🇲🇾", "role": "Player"},
        {"name": "something", "real_name": "Ilya Petrov", "flag": "🇷🇺", "role": "Player"},
    ],
    "staff": [
        {"name": "Tommy", "real_name": "Kumaresan Ramani", "flag": "🇸🇬", "role": "MANAGER"},
        {"name": "alecks", "real_name": "Alexandre Sallé", "flag": "🇫🇷", "role": "COACH"},
        {"name": "Wendler", "real_name": "Ashton Wendler", "flag": "🇺🇸", "role": "ASSISTANT COACH"},
        {"name": "Panda", "real_name": "Laijhun Cheng", "flag": "🇺🇸", "role": "PERFORMANCE COACH"},
    ]
}

PLAYER_F0RSAKEN = {
    "nickname": "f0rsakeN",
    "real_name": "Jason Susanto",
    "country": "Indonesia",
    "flag": "🇮🇩",
    "team": "Paper Rex",
    "agents_data": [
        {"agent": "Omen", "use": "(16) 59%", "rnd": 339, "rating": 0.98, "acs": 201.5, "kd": 1.02, "adr": 131.4, "kast": "76%", "kpr": 0.72, "apr": 0.40, "fkpr": 0.11, "fdpr": 0.08, "k": 245, "d": 241, "a": 136, "fk": 36, "fd": 26},
        {"agent": "Jett", "use": "(6) 22%", "rnd": 119, "rating": 1.10, "acs": 241.5, "kd": 1.20, "adr": 156.2, "kast": "71%", "kpr": 0.87, "apr": 0.25, "fkpr": 0.13, "fdpr": 0.14, "k": 103, "d": 86, "a": 30, "fk": 15, "fd": 17},
        {"agent": "Phoenix", "use": "(3) 11%", "rnd": 62, "rating": 1.22, "acs": 229.0, "kd": 1.19, "adr": 147.8, "kast": "77%", "kpr": 0.82, "apr": 0.47, "fkpr": 0.05, "fdpr": 0.05, "k": 51, "d": 43, "a": 29, "fk": 3, "fd": 3},
        {"agent": "Breach", "use": "(2) 7%", "rnd": 44, "rating": 1.04, "acs": 161.0, "kd": 0.92, "adr": 114.1, "kast": "82%", "kpr": 0.55, "apr": 0.61, "fkpr": 0.02, "fdpr": 0.05, "k": 24, "d": 26, "a": 27, "fk": 1, "fd": 2},
    ]
}
