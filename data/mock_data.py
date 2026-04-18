"""
data/mock_data.py
─────────────────
Complete realistic mock match for offline / demo mode.

Scenario:  RCB vs CSK, Match 14, IPL 2026
           Over 14, RCB batting 2nd, chasing 182
           Score: 98/3 after 13.2 overs
           Venue: M Chinnaswamy Stadium

Provides the same normalized dict structure as live_data.py so every
downstream consumer works identically in demo mode.
"""

MOCK_MATCH = {
    "id": "demo_rcb_csk_14",
    "title": "RCB vs CSK, Match 14, IPL 2026",
    "status": "live",
    "source": "mock",
    "venue": "M Chinnaswamy Stadium, Bengaluru",
    "toss": "CSK won the toss and elected to bat first",

    # ── Teams ────────────────────────────────────────────────────────
    "team_a": {
        "id": "rcb",
        "name": "Royal Challengers Bengaluru",
        "short": "RCB",
        "color": "#E25822",
    },
    "team_b": {
        "id": "csk",
        "name": "Chennai Super Kings",
        "short": "CSK",
        "color": "#FCCA06",
    },

    # ── Innings ──────────────────────────────────────────────────────
    "innings": [
        # Innings 1: CSK batted first — 181/6 in 20 overs
        {
            "inning_number": 1,
            "batting_team": "csk",
            "bowling_team": "rcb",
            "runs": 181,
            "wickets": 6,
            "overs": 20.0,
            "target": None,
            "batters": [
                {"name": "Ruturaj Gaikwad", "runs": 52, "balls": 38, "dismissed": True,
                 "dismissal": "c Kohli b Hasaranga"},
                {"name": "Devon Conway", "runs": 38, "balls": 28, "dismissed": True,
                 "dismissal": "b Siraj"},
                {"name": "Shivam Dube", "runs": 42, "balls": 25, "dismissed": True,
                 "dismissal": "c Maxwell b Hazlewood"},
                {"name": "Ravindra Jadeja", "runs": 22, "balls": 18, "dismissed": True,
                 "dismissal": "run out (Green)"},
                {"name": "MS Dhoni", "runs": 18, "balls": 8, "dismissed": False,
                 "dismissal": ""},
                {"name": "Moeen Ali", "runs": 5, "balls": 4, "dismissed": True,
                 "dismissal": "c Rawat b Ferguson"},
                {"name": "Daryl Mitchell", "runs": 2, "balls": 3, "dismissed": True,
                 "dismissal": "lbw b Hasaranga"},
                {"name": "Deepak Chahar", "runs": 0, "balls": 0, "dismissed": False,
                 "dismissal": ""},
            ],
            "bowlers": [
                {"name": "Mohammed Siraj", "overs": 4.0, "runs": 32, "wickets": 1, "econ": 8.0},
                {"name": "Josh Hazlewood", "overs": 4.0, "runs": 35, "wickets": 1, "econ": 8.75},
                {"name": "Yash Dayal", "overs": 3.0, "runs": 28, "wickets": 0, "econ": 9.33},
                {"name": "Wanindu Hasaranga", "overs": 4.0, "runs": 30, "wickets": 2, "econ": 7.5},
                {"name": "Cameron Green", "overs": 2.0, "runs": 22, "wickets": 0, "econ": 11.0},
                {"name": "Glenn Maxwell", "overs": 2.0, "runs": 18, "wickets": 0, "econ": 9.0},
                {"name": "Lockie Ferguson", "overs": 1.0, "runs": 12, "wickets": 1, "econ": 12.0},
            ],
            "last_6_balls": ["1", "4", "2", "0", "6", "1"],
        },
        # Innings 2: RCB batting — 98/3 after 13.2 overs, chasing 182
        {
            "inning_number": 2,
            "batting_team": "rcb",
            "bowling_team": "csk",
            "runs": 98,
            "wickets": 3,
            "overs": 13.2,
            "target": 182,
            "batters": [
                {"name": "Virat Kohli", "runs": 45, "balls": 32, "dismissed": False,
                 "dismissal": ""},
                {"name": "Faf du Plessis", "runs": 18, "balls": 14, "dismissed": True,
                 "dismissal": "c Jadeja b Pathirana"},
                {"name": "Rajat Patidar", "runs": 22, "balls": 16, "dismissed": True,
                 "dismissal": "b Theekshana"},
                {"name": "Glenn Maxwell", "runs": 5, "balls": 8, "dismissed": True,
                 "dismissal": "c Dhoni b Jadeja"},
                {"name": "Cameron Green", "runs": 6, "balls": 10, "dismissed": False,
                 "dismissal": ""},
            ],
            "bowlers": [
                {"name": "Deepak Chahar", "overs": 3.0, "runs": 22, "wickets": 0, "econ": 7.33},
                {"name": "Matheesha Pathirana", "overs": 3.0, "runs": 18, "wickets": 1, "econ": 6.0},
                {"name": "Maheesh Theekshana", "overs": 3.0, "runs": 24, "wickets": 1, "econ": 8.0},
                {"name": "Ravindra Jadeja", "overs": 3.2, "runs": 20, "wickets": 1, "econ": 6.0},
                {"name": "Shardul Thakur", "overs": 1.0, "runs": 12, "wickets": 0, "econ": 12.0},
            ],
            "last_6_balls": ["0", "1", "4", "W", "2", "1"],
        },
    ],

    # ── Playing 15: RCB (team_a) ─────────────────────────────────────
    "squad_a": [
        # Playing 11
        {"name": "Virat Kohli", "role": "bat", "is_playing_11": True},
        {"name": "Faf du Plessis", "role": "bat", "is_playing_11": True},
        {"name": "Rajat Patidar", "role": "bat", "is_playing_11": True},
        {"name": "Glenn Maxwell", "role": "allrounder", "is_playing_11": True},
        {"name": "Dinesh Karthik", "role": "wk-bat", "is_playing_11": True},
        {"name": "Cameron Green", "role": "allrounder", "is_playing_11": True},
        {"name": "Wanindu Hasaranga", "role": "bowl", "is_playing_11": True},
        {"name": "Josh Hazlewood", "role": "bowl", "is_playing_11": True},
        {"name": "Mohammed Siraj", "role": "bowl", "is_playing_11": True},
        {"name": "Yash Dayal", "role": "bowl", "is_playing_11": True},
        {"name": "Lockie Ferguson", "role": "bowl", "is_playing_11": True},
        # Bench (4 players)
        {"name": "Mahipal Lomror", "role": "allrounder", "is_playing_11": False},
        {"name": "Anuj Rawat", "role": "wk-bat", "is_playing_11": False},
        {"name": "Karn Sharma", "role": "bowl", "is_playing_11": False},
        {"name": "Suyash Prabhudessai", "role": "bat", "is_playing_11": False},
    ],

    # ── Playing 15: CSK (team_b) ─────────────────────────────────────
    "squad_b": [
        # Playing 11
        {"name": "Ruturaj Gaikwad", "role": "bat", "is_playing_11": True},
        {"name": "Devon Conway", "role": "bat", "is_playing_11": True},
        {"name": "Shivam Dube", "role": "allrounder", "is_playing_11": True},
        {"name": "Ravindra Jadeja", "role": "allrounder", "is_playing_11": True},
        {"name": "MS Dhoni", "role": "wk-bat", "is_playing_11": True},
        {"name": "Moeen Ali", "role": "allrounder", "is_playing_11": True},
        {"name": "Daryl Mitchell", "role": "allrounder", "is_playing_11": True},
        {"name": "Deepak Chahar", "role": "bowl", "is_playing_11": True},
        {"name": "Matheesha Pathirana", "role": "bowl", "is_playing_11": True},
        {"name": "Maheesh Theekshana", "role": "bowl", "is_playing_11": True},
        {"name": "Shardul Thakur", "role": "allrounder", "is_playing_11": True},
        # Bench (4 players)
        {"name": "Rachin Ravindra", "role": "allrounder", "is_playing_11": False},
        {"name": "Ajinkya Rahane", "role": "bat", "is_playing_11": False},
        {"name": "Mitchell Santner", "role": "allrounder", "is_playing_11": False},
        {"name": "Tushar Deshpande", "role": "bowl", "is_playing_11": False},
    ],
}


# ── Schedule (for sidebar match selector) ────────────────────────────
MOCK_SCHEDULE = [
    {
        "id": "demo_rcb_csk_14",
        "title": "RCB vs CSK, Match 14, IPL 2026",
        "status": "live",
        "source": "mock",
        "team_a": {"id": "rcb", "short": "RCB"},
        "team_b": {"id": "csk", "short": "CSK"},
    },
    {
        "id": "demo_mi_kkr_15",
        "title": "MI vs KKR, Match 15, IPL 2026",
        "status": "upcoming",
        "source": "mock",
        "team_a": {"id": "mi", "short": "MI"},
        "team_b": {"id": "kkr", "short": "KKR"},
    },
]


def get_mock_match() -> dict:
    """
    Return the full mock match dict.

    Returns
    -------
    dict   normalized match structure identical to live_data output.
    """
    return MOCK_MATCH.copy()


def get_mock_schedule() -> list[dict]:
    """
    Return mock schedule list.

    Returns
    -------
    list[dict]   list of match summary dicts.
    """
    return MOCK_SCHEDULE.copy()
