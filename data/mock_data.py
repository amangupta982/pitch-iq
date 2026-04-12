"""data/mock_data.py — demo scorecard used when live data is unavailable."""

MOCK_SCORECARD = {
    "match_id": "demo_rcb_csk",
    "title":    "RCB vs CSK, IPL 2026 — Demo",
    "status":   "In Progress",
    "toss":     "RCB won the toss and elected to bat",
    "venue":    "Chinnaswamy, Bengaluru",
    "innings": [
        {
            "team":  "Royal Challengers Bengaluru",
            "total": "148/4",
            "overs": "16.0",
            "batters": [
                {"name": "Virat Kohli",    "runs": 62, "balls": 44, "fours": 6, "sixes": 2, "sr": 140.9, "dismissal": "c Conway b Pathirana", "out": True},
                {"name": "Faf du Plessis", "runs": 18, "balls": 15, "fours": 2, "sixes": 0, "sr": 120.0, "dismissal": "b Chahar",             "out": True},
                {"name": "Rajat Patidar",  "runs": 34, "balls": 22, "fours": 3, "sixes": 1, "sr": 154.5, "dismissal": "batting",               "out": False},
                {"name": "Glenn Maxwell",  "runs": 22, "balls": 12, "fours": 1, "sixes": 2, "sr": 183.3, "dismissal": "batting",               "out": False},
            ],
            "bowlers": [
                {"name": "Deepak Chahar",       "overs": 4.0, "maidens": 0, "runs": 28, "wickets": 1, "economy": 7.0,  "wides": 1, "noballs": 0},
                {"name": "Ravindra Jadeja",     "overs": 4.0, "maidens": 0, "runs": 24, "wickets": 1, "economy": 6.0,  "wides": 0, "noballs": 0},
                {"name": "Matheesha Pathirana", "overs": 4.0, "maidens": 0, "runs": 42, "wickets": 2, "economy": 10.5, "wides": 2, "noballs": 0},
                {"name": "Maheesh Theekshana",  "overs": 4.0, "maidens": 0, "runs": 36, "wickets": 0, "economy": 9.0,  "wides": 0, "noballs": 0},
            ],
        }
    ],
    "source": "mock",
}
