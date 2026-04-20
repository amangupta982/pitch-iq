"""
data/teams_db.py
────────────────
IPL 2026 — All 10 franchise profiles.

Each team dict contains:
  id          short lowercase identifier
  name        official franchise name
  short       3-letter abbreviation used on scoreboards
  color       primary hex brand color
  home_venue  home stadium name
  players     list of player-name strings (Playing-15 pool)

Used by squad_resolver to fuzzy-match API names → known rosters.
"""

TEAMS = {
    "rcb": {
        "id": "rcb",
        "name": "Royal Challengers Bengaluru",
        "short": "RCB",
        "color": "#E25822",
        "home_venue": "M Chinnaswamy Stadium",
        "players": [
            "Virat Kohli", "Faf du Plessis", "Rajat Patidar",
            "Glenn Maxwell", "Dinesh Karthik", "Mahipal Lomror",
            "Anuj Rawat", "Cameron Green", "Wanindu Hasaranga",
            "Josh Hazlewood", "Mohammed Siraj", "Yash Dayal",
            "Karn Sharma", "Suyash Prabhudessai", "Lockie Ferguson",
        ],
    },
    "csk": {
        "id": "csk",
        "name": "Chennai Super Kings",
        "short": "CSK",
        "color": "#FCCA06",
        "home_venue": "MA Chidambaram Stadium",
        "players": [
            "Ruturaj Gaikwad", "Devon Conway", "Shivam Dube",
            "Ravindra Jadeja", "MS Dhoni", "Moeen Ali",
            "Daryl Mitchell", "Deepak Chahar", "Tushar Deshpande",
            "Matheesha Pathirana", "Maheesh Theekshana",
            "Rachin Ravindra", "Ajinkya Rahane", "Shardul Thakur",
            "Mitchell Santner",
        ],
    },
    "mi": {
        "id": "mi",
        "name": "Mumbai Indians",
        "short": "MI",
        "color": "#004BA0",
        "home_venue": "Wankhede Stadium",
        "players": [
            "Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav",
            "Tim David", "Hardik Pandya", "Tilak Varma",
            "Nehal Wadhera", "Jasprit Bumrah", "Trent Boult",
            "Piyush Chawla", "Kumar Kartikeya", "Gerald Coetzee",
            "Romario Shepherd", "Arjun Tendulkar", "Naman Dhir",
        ],
    },
    "kkr": {
        "id": "kkr",
        "name": "Kolkata Knight Riders",
        "short": "KKR",
        "color": "#3A225D",
        "home_venue": "Eden Gardens",
        "players": [
            "Shreyas Iyer", "Venkatesh Iyer", "Nitish Rana",
            "Andre Russell", "Sunil Narine", "Rinku Singh",
            "Phil Salt", "Mitchell Starc", "Varun Chakravarthy",
            "Harshit Rana", "Ramandeep Singh", "Anrich Nortje",
            "Manish Pandey", "Suyash Sharma", "Angkrish Raghuvanshi",
        ],
    },
    "srh": {
        "id": "srh",
        "name": "Sunrisers Hyderabad",
        "short": "SRH",
        "color": "#FF822A",
        "home_venue": "Rajiv Gandhi Intl Stadium",
        "players": [
            "Travis Head", "Abhishek Sharma", "Heinrich Klaasen",
            "Aiden Markram", "Pat Cummins", "Bhuvneshwar Kumar",
            "Shahbaz Ahmed", "Rahul Tripathi", "Marco Jansen",
            "T Natarajan", "Umran Malik", "Washington Sundar",
            "Abdul Samad", "Glenn Phillips", "Jaydev Unadkat",
        ],
    },
    "lsg": {
        "id": "lsg",
        "name": "Lucknow Super Giants",
        "short": "LSG",
        "color": "#ACE5F0",
        "home_venue": "BRSABV Ekana Stadium",
        "players": [
            "KL Rahul", "Quinton de Kock", "Nicholas Pooran",
            "Marcus Stoinis", "Ayush Badoni", "Krunal Pandya",
            "Deepak Hooda", "Mark Wood", "Ravi Bishnoi",
            "Avesh Khan", "Mohsin Khan", "Naveen-ul-Haq",
            "Devdutt Padikkal", "Manan Vohra", "Yash Thakur",
        ],
    },
    "dc": {
        "id": "dc",
        "name": "Delhi Capitals",
        "short": "DC",
        "color": "#17479E",
        "home_venue": "Arun Jaitley Stadium",
        "players": [
            "David Warner", "Jake Fraser-McGurk", "Rishabh Pant",
            "Axar Patel", "Tristan Stubbs", "Prithvi Shaw",
            "Abishek Porel", "Anrich Nortje", "Kuldeep Yadav",
            "Khaleel Ahmed", "Ishant Sharma", "Mitchell Marsh",
            "Mukesh Kumar", "Rasikh Salam", "Sumit Kumar",
        ],
    },
    "rr": {
        "id": "rr",
        "name": "Rajasthan Royals",
        "short": "RR",
        "color": "#EA1A85",
        "home_venue": "Sawai Mansingh Stadium",
        "players": [
            "Sanju Samson", "Yashasvi Jaiswal", "Jos Buttler",
            "Shimron Hetmyer", "Dhruv Jurel", "Riyan Parag",
            "Ravichandran Ashwin", "Trent Boult", "Yuzvendra Chahal",
            "Sandeep Sharma", "Avesh Khan", "Donovan Ferreira",
            "Kunal Rathore", "Nandre Burger", "Tom Kohler-Cadmore",
        ],
    },
    "pbks": {
        "id": "pbks",
        "name": "Punjab Kings",
        "short": "PBKS",
        "color": "#DD1F2D",
        "home_venue": "PCA New Stadium Mullanpur",
        "players": [
            "Shikhar Dhawan", "Jonny Bairstow", "Liam Livingstone",
            "Sam Curran", "Jitesh Sharma", "Shahrukh Khan",
            "Harpreet Brar", "Arshdeep Singh", "Kagiso Rabada",
            "Rahul Chahar", "Nathan Ellis", "Atharva Taide",
            "Prabhsimran Singh", "Vidwath Kaverappa", "Rishi Dhawan",
        ],
    },
    "gt": {
        "id": "gt",
        "name": "Gujarat Titans",
        "short": "GT",
        "color": "#1C3879",
        "home_venue": "Narendra Modi Stadium",
        "players": [
            "Shubman Gill", "Wriddhiman Saha", "Sai Sudharsan",
            "David Miller", "Rashid Khan", "Rahul Tewatia",
            "Vijay Shankar", "Mohammed Shami", "Josh Little",
            "Noor Ahmad", "Umesh Yadav", "Kane Williamson",
            "Matthew Wade", "Azmatullah Omarzai", "Mohit Sharma",
        ],
    },
}


def get_team(team_id: str) -> dict:
    """
    Return the team dict for a given lowercase team id.

    Parameters
    ----------
    team_id : str   e.g. "rcb", "csk"

    Returns
    -------
    dict   team profile or a minimal fallback dict if not found.
    """
    return TEAMS.get(team_id, {"id": team_id, "name": team_id.upper(),
                                "short": team_id.upper(), "color": "#666",
                                "home_venue": "Unknown", "players": []})


def get_all_teams() -> dict:
    """Return the full TEAMS dict."""
    return TEAMS


def find_team_by_name(name: str) -> dict | None:
    """
    Fuzzy-find a team by its full or short name.

    Uses resolve_team_id() from squad_resolver for robust matching
    across all 10 IPL teams including abbreviations and variations.

    Parameters
    ----------
    name : str   e.g. "Chennai Super Kings", "CSK", "csk",
                       "Kolkata Knight Rid..."

    Returns
    -------
    dict | None   team dict if found, else None.
    """
    if not name or not name.strip():
        return None

    # Quick exact match first (avoid circular import overhead)
    low = name.strip().lower()
    for tid, t in TEAMS.items():
        if low in (tid, t["short"].lower(), t["name"].lower()):
            return t

    # Use the robust resolver for fuzzy/substring/alias matching
    try:
        from core.squad_resolver import resolve_team_id
        team_id = resolve_team_id(name)
        if team_id != "unk":
            return TEAMS.get(team_id)
    except ImportError:
        pass  # Fallback if circular import occurs during init

    # Last resort: partial match
    for tid, t in TEAMS.items():
        if low in t["name"].lower():
            return t
    return None
