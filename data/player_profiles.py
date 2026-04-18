"""
data/player_profiles.py
───────────────────────
IPL 2026 — Detailed statistical profiles for ~150 players across all
10 franchises.

Every profile contains:
  name          full canonical name (used as match key everywhere)
  team          lowercase team id
  hand          "R" or "L" batting hand
  role          "bat" | "bowl" | "allrounder" | "wk-bat"
  avg           batting average (T20 / IPL career)
  sr            batting strike rate
  powerplay_sr  strike rate in overs 1-6
  death_sr      strike rate in overs 17-20
  chase_sr      strike rate when chasing
  vs_pace       0-100 rating vs pace bowling
  vs_spin       0-100 rating vs spin bowling
  form          0-100 current-season form index
  econ          bowling economy (None for pure batters)
  death_econ    death-overs economy (None for non-bowlers)
  wkts          wickets this season (None for non-bowlers)
  bowling_type  "pace" | "medium" | "offspin" | "legspin" | "left-arm-spin" | None

Used by squad_resolver to merge into live player dicts.
"""

PLAYER_PROFILES: dict[str, dict] = {

    # ── RCB ──────────────────────────────────────────────────────────
    "Virat Kohli": {
        "name": "Virat Kohli", "team": "rcb", "hand": "R", "role": "bat",
        "avg": 52, "sr": 138, "powerplay_sr": 145, "death_sr": 148,
        "chase_sr": 142, "vs_pace": 72, "vs_spin": 85, "form": 92,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Faf du Plessis": {
        "name": "Faf du Plessis", "team": "rcb", "hand": "R", "role": "bat",
        "avg": 36, "sr": 140, "powerplay_sr": 152, "death_sr": 155,
        "chase_sr": 135, "vs_pace": 78, "vs_spin": 70, "form": 74,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Rajat Patidar": {
        "name": "Rajat Patidar", "team": "rcb", "hand": "R", "role": "bat",
        "avg": 38, "sr": 155, "powerplay_sr": 148, "death_sr": 170,
        "chase_sr": 150, "vs_pace": 74, "vs_spin": 80, "form": 85,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Glenn Maxwell": {
        "name": "Glenn Maxwell", "team": "rcb", "hand": "R", "role": "allrounder",
        "avg": 30, "sr": 158, "powerplay_sr": 140, "death_sr": 185,
        "chase_sr": 160, "vs_pace": 68, "vs_spin": 82, "form": 70,
        "econ": 8.5, "death_econ": 10.0, "wkts": 4, "bowling_type": "offspin",
    },
    "Dinesh Karthik": {
        "name": "Dinesh Karthik", "team": "rcb", "hand": "R", "role": "wk-bat",
        "avg": 28, "sr": 152, "powerplay_sr": 125, "death_sr": 190,
        "chase_sr": 155, "vs_pace": 70, "vs_spin": 65, "form": 68,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Mahipal Lomror": {
        "name": "Mahipal Lomror", "team": "rcb", "hand": "L", "role": "allrounder",
        "avg": 22, "sr": 140, "powerplay_sr": 132, "death_sr": 155,
        "chase_sr": 138, "vs_pace": 60, "vs_spin": 72, "form": 60,
        "econ": 8.2, "death_econ": 9.5, "wkts": 3, "bowling_type": "left-arm-spin",
    },
    "Anuj Rawat": {
        "name": "Anuj Rawat", "team": "rcb", "hand": "L", "role": "wk-bat",
        "avg": 18, "sr": 128, "powerplay_sr": 135, "death_sr": 140,
        "chase_sr": 130, "vs_pace": 55, "vs_spin": 58, "form": 50,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Cameron Green": {
        "name": "Cameron Green", "team": "rcb", "hand": "R", "role": "allrounder",
        "avg": 32, "sr": 148, "powerplay_sr": 150, "death_sr": 160,
        "chase_sr": 145, "vs_pace": 75, "vs_spin": 65, "form": 78,
        "econ": 8.0, "death_econ": 9.2, "wkts": 6, "bowling_type": "pace",
    },
    "Wanindu Hasaranga": {
        "name": "Wanindu Hasaranga", "team": "rcb", "hand": "R", "role": "bowl",
        "avg": 12, "sr": 135, "powerplay_sr": 120, "death_sr": 145,
        "chase_sr": 130, "vs_pace": 40, "vs_spin": 45, "form": 82,
        "econ": 7.2, "death_econ": 8.5, "wkts": 14, "bowling_type": "legspin",
    },
    "Josh Hazlewood": {
        "name": "Josh Hazlewood", "team": "rcb", "hand": "L", "role": "bowl",
        "avg": 8, "sr": 95, "powerplay_sr": 80, "death_sr": 100,
        "chase_sr": 90, "vs_pace": 20, "vs_spin": 25, "form": 80,
        "econ": 7.8, "death_econ": 8.8, "wkts": 12, "bowling_type": "pace",
    },
    "Mohammed Siraj": {
        "name": "Mohammed Siraj", "team": "rcb", "hand": "R", "role": "bowl",
        "avg": 6, "sr": 90, "powerplay_sr": 75, "death_sr": 95,
        "chase_sr": 85, "vs_pace": 15, "vs_spin": 20, "form": 76,
        "econ": 8.2, "death_econ": 9.5, "wkts": 10, "bowling_type": "pace",
    },
    "Yash Dayal": {
        "name": "Yash Dayal", "team": "rcb", "hand": "L", "role": "bowl",
        "avg": 5, "sr": 85, "powerplay_sr": 70, "death_sr": 90,
        "chase_sr": 80, "vs_pace": 10, "vs_spin": 15, "form": 72,
        "econ": 8.5, "death_econ": 10.0, "wkts": 8, "bowling_type": "pace",
    },
    "Karn Sharma": {
        "name": "Karn Sharma", "team": "rcb", "hand": "R", "role": "bowl",
        "avg": 10, "sr": 110, "powerplay_sr": 100, "death_sr": 120,
        "chase_sr": 105, "vs_pace": 30, "vs_spin": 35, "form": 55,
        "econ": 7.8, "death_econ": 9.0, "wkts": 5, "bowling_type": "legspin",
    },
    "Suyash Prabhudessai": {
        "name": "Suyash Prabhudessai", "team": "rcb", "hand": "R", "role": "bat",
        "avg": 20, "sr": 142, "powerplay_sr": 138, "death_sr": 160,
        "chase_sr": 140, "vs_pace": 62, "vs_spin": 58, "form": 58,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Lockie Ferguson": {
        "name": "Lockie Ferguson", "team": "rcb", "hand": "R", "role": "bowl",
        "avg": 7, "sr": 100, "powerplay_sr": 85, "death_sr": 110,
        "chase_sr": 95, "vs_pace": 18, "vs_spin": 22, "form": 84,
        "econ": 7.5, "death_econ": 8.2, "wkts": 15, "bowling_type": "pace",
    },

    # ── CSK ──────────────────────────────────────────────────────────
    "Ruturaj Gaikwad": {
        "name": "Ruturaj Gaikwad", "team": "csk", "hand": "R", "role": "bat",
        "avg": 42, "sr": 135, "powerplay_sr": 142, "death_sr": 150,
        "chase_sr": 138, "vs_pace": 75, "vs_spin": 80, "form": 88,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Devon Conway": {
        "name": "Devon Conway", "team": "csk", "hand": "L", "role": "bat",
        "avg": 38, "sr": 132, "powerplay_sr": 138, "death_sr": 145,
        "chase_sr": 130, "vs_pace": 78, "vs_spin": 72, "form": 80,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Shivam Dube": {
        "name": "Shivam Dube", "team": "csk", "hand": "L", "role": "allrounder",
        "avg": 30, "sr": 148, "powerplay_sr": 135, "death_sr": 175,
        "chase_sr": 155, "vs_pace": 72, "vs_spin": 60, "form": 82,
        "econ": 9.0, "death_econ": 10.5, "wkts": 2, "bowling_type": "medium",
    },
    "Ravindra Jadeja": {
        "name": "Ravindra Jadeja", "team": "csk", "hand": "L", "role": "allrounder",
        "avg": 26, "sr": 132, "powerplay_sr": 120, "death_sr": 165,
        "chase_sr": 140, "vs_pace": 65, "vs_spin": 55, "form": 75,
        "econ": 7.0, "death_econ": 8.0, "wkts": 10, "bowling_type": "left-arm-spin",
    },
    "MS Dhoni": {
        "name": "MS Dhoni", "team": "csk", "hand": "R", "role": "wk-bat",
        "avg": 35, "sr": 148, "powerplay_sr": 125, "death_sr": 195,
        "chase_sr": 152, "vs_pace": 80, "vs_spin": 70, "form": 65,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Moeen Ali": {
        "name": "Moeen Ali", "team": "csk", "hand": "L", "role": "allrounder",
        "avg": 25, "sr": 145, "powerplay_sr": 155, "death_sr": 160,
        "chase_sr": 148, "vs_pace": 70, "vs_spin": 68, "form": 72,
        "econ": 7.5, "death_econ": 9.0, "wkts": 7, "bowling_type": "offspin",
    },
    "Daryl Mitchell": {
        "name": "Daryl Mitchell", "team": "csk", "hand": "R", "role": "allrounder",
        "avg": 28, "sr": 130, "powerplay_sr": 128, "death_sr": 145,
        "chase_sr": 132, "vs_pace": 72, "vs_spin": 65, "form": 70,
        "econ": 8.5, "death_econ": 9.8, "wkts": 3, "bowling_type": "medium",
    },
    "Deepak Chahar": {
        "name": "Deepak Chahar", "team": "csk", "hand": "R", "role": "bowl",
        "avg": 8, "sr": 105, "powerplay_sr": 90, "death_sr": 115,
        "chase_sr": 100, "vs_pace": 20, "vs_spin": 25, "form": 78,
        "econ": 7.4, "death_econ": 9.0, "wkts": 11, "bowling_type": "pace",
    },
    "Tushar Deshpande": {
        "name": "Tushar Deshpande", "team": "csk", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 68,
        "econ": 8.8, "death_econ": 10.2, "wkts": 9, "bowling_type": "pace",
    },
    "Matheesha Pathirana": {
        "name": "Matheesha Pathirana", "team": "csk", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 75, "powerplay_sr": 60, "death_sr": 85,
        "chase_sr": 70, "vs_pace": 8, "vs_spin": 10, "form": 88,
        "econ": 7.0, "death_econ": 7.5, "wkts": 16, "bowling_type": "pace",
    },
    "Maheesh Theekshana": {
        "name": "Maheesh Theekshana", "team": "csk", "hand": "R", "role": "bowl",
        "avg": 6, "sr": 90, "powerplay_sr": 78, "death_sr": 95,
        "chase_sr": 82, "vs_pace": 15, "vs_spin": 20, "form": 76,
        "econ": 7.2, "death_econ": 8.5, "wkts": 10, "bowling_type": "offspin",
    },
    "Rachin Ravindra": {
        "name": "Rachin Ravindra", "team": "csk", "hand": "L", "role": "allrounder",
        "avg": 30, "sr": 138, "powerplay_sr": 145, "death_sr": 150,
        "chase_sr": 140, "vs_pace": 72, "vs_spin": 68, "form": 78,
        "econ": 7.8, "death_econ": 9.0, "wkts": 4, "bowling_type": "left-arm-spin",
    },
    "Ajinkya Rahane": {
        "name": "Ajinkya Rahane", "team": "csk", "hand": "R", "role": "bat",
        "avg": 28, "sr": 122, "powerplay_sr": 128, "death_sr": 130,
        "chase_sr": 125, "vs_pace": 70, "vs_spin": 74, "form": 62,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Shardul Thakur": {
        "name": "Shardul Thakur", "team": "csk", "hand": "R", "role": "allrounder",
        "avg": 14, "sr": 130, "powerplay_sr": 115, "death_sr": 155,
        "chase_sr": 135, "vs_pace": 35, "vs_spin": 40, "form": 65,
        "econ": 8.5, "death_econ": 9.8, "wkts": 8, "bowling_type": "pace",
    },
    "Mitchell Santner": {
        "name": "Mitchell Santner", "team": "csk", "hand": "L", "role": "allrounder",
        "avg": 15, "sr": 118, "powerplay_sr": 110, "death_sr": 135,
        "chase_sr": 120, "vs_pace": 40, "vs_spin": 50, "form": 60,
        "econ": 7.0, "death_econ": 8.0, "wkts": 6, "bowling_type": "left-arm-spin",
    },

    # ── MI ───────────────────────────────────────────────────────────
    "Rohit Sharma": {
        "name": "Rohit Sharma", "team": "mi", "hand": "R", "role": "bat",
        "avg": 48, "sr": 140, "powerplay_sr": 155, "death_sr": 155,
        "chase_sr": 142, "vs_pace": 82, "vs_spin": 78, "form": 85,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Ishan Kishan": {
        "name": "Ishan Kishan", "team": "mi", "hand": "L", "role": "wk-bat",
        "avg": 30, "sr": 138, "powerplay_sr": 148, "death_sr": 152,
        "chase_sr": 140, "vs_pace": 70, "vs_spin": 65, "form": 72,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Suryakumar Yadav": {
        "name": "Suryakumar Yadav", "team": "mi", "hand": "R", "role": "bat",
        "avg": 38, "sr": 162, "powerplay_sr": 150, "death_sr": 190,
        "chase_sr": 165, "vs_pace": 78, "vs_spin": 85, "form": 90,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Tim David": {
        "name": "Tim David", "team": "mi", "hand": "R", "role": "bat",
        "avg": 24, "sr": 165, "powerplay_sr": 140, "death_sr": 200,
        "chase_sr": 170, "vs_pace": 75, "vs_spin": 60, "form": 78,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Hardik Pandya": {
        "name": "Hardik Pandya", "team": "mi", "hand": "R", "role": "allrounder",
        "avg": 30, "sr": 150, "powerplay_sr": 138, "death_sr": 180,
        "chase_sr": 158, "vs_pace": 72, "vs_spin": 68, "form": 80,
        "econ": 8.2, "death_econ": 9.5, "wkts": 8, "bowling_type": "pace",
    },
    "Tilak Varma": {
        "name": "Tilak Varma", "team": "mi", "hand": "L", "role": "bat",
        "avg": 35, "sr": 142, "powerplay_sr": 135, "death_sr": 162,
        "chase_sr": 145, "vs_pace": 74, "vs_spin": 80, "form": 86,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Nehal Wadhera": {
        "name": "Nehal Wadhera", "team": "mi", "hand": "R", "role": "bat",
        "avg": 22, "sr": 138, "powerplay_sr": 130, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 60, "vs_spin": 55, "form": 62,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Jasprit Bumrah": {
        "name": "Jasprit Bumrah", "team": "mi", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 10, "vs_spin": 12, "form": 95,
        "econ": 6.5, "death_econ": 6.8, "wkts": 18, "bowling_type": "pace",
    },
    "Trent Boult": {
        "name": "Trent Boult", "team": "mi", "hand": "L", "role": "bowl",
        "avg": 6, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 12, "vs_spin": 15, "form": 82,
        "econ": 7.5, "death_econ": 8.8, "wkts": 12, "bowling_type": "pace",
    },
    "Piyush Chawla": {
        "name": "Piyush Chawla", "team": "mi", "hand": "R", "role": "bowl",
        "avg": 8, "sr": 95, "powerplay_sr": 80, "death_sr": 105,
        "chase_sr": 90, "vs_pace": 20, "vs_spin": 25, "form": 58,
        "econ": 7.8, "death_econ": 9.2, "wkts": 6, "bowling_type": "legspin",
    },
    "Kumar Kartikeya": {
        "name": "Kumar Kartikeya", "team": "mi", "hand": "L", "role": "bowl",
        "avg": 5, "sr": 85, "powerplay_sr": 72, "death_sr": 95,
        "chase_sr": 80, "vs_pace": 10, "vs_spin": 15, "form": 70,
        "econ": 7.5, "death_econ": 8.8, "wkts": 8, "bowling_type": "left-arm-spin",
    },
    "Gerald Coetzee": {
        "name": "Gerald Coetzee", "team": "mi", "hand": "R", "role": "bowl",
        "avg": 7, "sr": 110, "powerplay_sr": 95, "death_sr": 125,
        "chase_sr": 105, "vs_pace": 18, "vs_spin": 20, "form": 75,
        "econ": 8.5, "death_econ": 9.8, "wkts": 10, "bowling_type": "pace",
    },
    "Romario Shepherd": {
        "name": "Romario Shepherd", "team": "mi", "hand": "R", "role": "allrounder",
        "avg": 16, "sr": 145, "powerplay_sr": 130, "death_sr": 170,
        "chase_sr": 150, "vs_pace": 40, "vs_spin": 35, "form": 60,
        "econ": 8.8, "death_econ": 10.0, "wkts": 5, "bowling_type": "pace",
    },
    "Arjun Tendulkar": {
        "name": "Arjun Tendulkar", "team": "mi", "hand": "L", "role": "allrounder",
        "avg": 10, "sr": 115, "powerplay_sr": 105, "death_sr": 125,
        "chase_sr": 110, "vs_pace": 30, "vs_spin": 28, "form": 45,
        "econ": 9.0, "death_econ": 10.5, "wkts": 3, "bowling_type": "pace",
    },
    "Naman Dhir": {
        "name": "Naman Dhir", "team": "mi", "hand": "R", "role": "bat",
        "avg": 18, "sr": 135, "powerplay_sr": 130, "death_sr": 148,
        "chase_sr": 132, "vs_pace": 55, "vs_spin": 50, "form": 52,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },

    # ── KKR ──────────────────────────────────────────────────────────
    "Shreyas Iyer": {
        "name": "Shreyas Iyer", "team": "kkr", "hand": "R", "role": "bat",
        "avg": 38, "sr": 132, "powerplay_sr": 128, "death_sr": 148,
        "chase_sr": 135, "vs_pace": 72, "vs_spin": 60, "form": 82,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Venkatesh Iyer": {
        "name": "Venkatesh Iyer", "team": "kkr", "hand": "L", "role": "allrounder",
        "avg": 26, "sr": 140, "powerplay_sr": 148, "death_sr": 155,
        "chase_sr": 142, "vs_pace": 68, "vs_spin": 62, "form": 74,
        "econ": 8.8, "death_econ": 10.0, "wkts": 3, "bowling_type": "medium",
    },
    "Nitish Rana": {
        "name": "Nitish Rana", "team": "kkr", "hand": "L", "role": "bat",
        "avg": 28, "sr": 135, "powerplay_sr": 140, "death_sr": 150,
        "chase_sr": 138, "vs_pace": 65, "vs_spin": 72, "form": 68,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Andre Russell": {
        "name": "Andre Russell", "team": "kkr", "hand": "R", "role": "allrounder",
        "avg": 28, "sr": 178, "powerplay_sr": 155, "death_sr": 210,
        "chase_sr": 185, "vs_pace": 82, "vs_spin": 70, "form": 85,
        "econ": 8.8, "death_econ": 9.5, "wkts": 8, "bowling_type": "pace",
    },
    "Sunil Narine": {
        "name": "Sunil Narine", "team": "kkr", "hand": "L", "role": "allrounder",
        "avg": 22, "sr": 168, "powerplay_sr": 180, "death_sr": 160,
        "chase_sr": 165, "vs_pace": 75, "vs_spin": 60, "form": 88,
        "econ": 6.5, "death_econ": 7.5, "wkts": 12, "bowling_type": "offspin",
    },
    "Rinku Singh": {
        "name": "Rinku Singh", "team": "kkr", "hand": "L", "role": "bat",
        "avg": 32, "sr": 155, "powerplay_sr": 138, "death_sr": 185,
        "chase_sr": 165, "vs_pace": 78, "vs_spin": 68, "form": 88,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Phil Salt": {
        "name": "Phil Salt", "team": "kkr", "hand": "R", "role": "wk-bat",
        "avg": 32, "sr": 162, "powerplay_sr": 175, "death_sr": 170,
        "chase_sr": 160, "vs_pace": 80, "vs_spin": 65, "form": 86,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Mitchell Starc": {
        "name": "Mitchell Starc", "team": "kkr", "hand": "L", "role": "bowl",
        "avg": 6, "sr": 85, "powerplay_sr": 70, "death_sr": 95,
        "chase_sr": 80, "vs_pace": 12, "vs_spin": 15, "form": 82,
        "econ": 7.8, "death_econ": 8.5, "wkts": 14, "bowling_type": "pace",
    },
    "Varun Chakravarthy": {
        "name": "Varun Chakravarthy", "team": "kkr", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 8, "vs_spin": 12, "form": 88,
        "econ": 6.8, "death_econ": 7.8, "wkts": 16, "bowling_type": "legspin",
    },
    "Harshit Rana": {
        "name": "Harshit Rana", "team": "kkr", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 68, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 76,
        "econ": 8.0, "death_econ": 9.2, "wkts": 10, "bowling_type": "pace",
    },
    "Ramandeep Singh": {
        "name": "Ramandeep Singh", "team": "kkr", "hand": "R", "role": "allrounder",
        "avg": 18, "sr": 148, "powerplay_sr": 135, "death_sr": 168,
        "chase_sr": 150, "vs_pace": 55, "vs_spin": 50, "form": 65,
        "econ": 9.2, "death_econ": 10.5, "wkts": 2, "bowling_type": "medium",
    },
    "Anrich Nortje": {
        "name": "Anrich Nortje", "team": "kkr", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 78,
        "econ": 7.8, "death_econ": 8.5, "wkts": 12, "bowling_type": "pace",
    },
    "Manish Pandey": {
        "name": "Manish Pandey", "team": "kkr", "hand": "R", "role": "bat",
        "avg": 30, "sr": 120, "powerplay_sr": 118, "death_sr": 132,
        "chase_sr": 125, "vs_pace": 68, "vs_spin": 72, "form": 55,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Suyash Sharma": {
        "name": "Suyash Sharma", "team": "kkr", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 65, "powerplay_sr": 50, "death_sr": 75,
        "chase_sr": 60, "vs_pace": 8, "vs_spin": 10, "form": 62,
        "econ": 7.5, "death_econ": 8.8, "wkts": 5, "bowling_type": "legspin",
    },
    "Angkrish Raghuvanshi": {
        "name": "Angkrish Raghuvanshi", "team": "kkr", "hand": "R", "role": "bat",
        "avg": 18, "sr": 130, "powerplay_sr": 135, "death_sr": 142,
        "chase_sr": 128, "vs_pace": 55, "vs_spin": 52, "form": 50,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },

    # ── SRH ──────────────────────────────────────────────────────────
    "Travis Head": {
        "name": "Travis Head", "team": "srh", "hand": "L", "role": "bat",
        "avg": 38, "sr": 162, "powerplay_sr": 175, "death_sr": 170,
        "chase_sr": 158, "vs_pace": 82, "vs_spin": 72, "form": 90,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Abhishek Sharma": {
        "name": "Abhishek Sharma", "team": "srh", "hand": "L", "role": "allrounder",
        "avg": 26, "sr": 155, "powerplay_sr": 168, "death_sr": 160,
        "chase_sr": 150, "vs_pace": 70, "vs_spin": 62, "form": 82,
        "econ": 8.0, "death_econ": 9.5, "wkts": 3, "bowling_type": "left-arm-spin",
    },
    "Heinrich Klaasen": {
        "name": "Heinrich Klaasen", "team": "srh", "hand": "R", "role": "wk-bat",
        "avg": 35, "sr": 172, "powerplay_sr": 148, "death_sr": 210,
        "chase_sr": 178, "vs_pace": 75, "vs_spin": 88, "form": 92,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Aiden Markram": {
        "name": "Aiden Markram", "team": "srh", "hand": "R", "role": "allrounder",
        "avg": 28, "sr": 130, "powerplay_sr": 125, "death_sr": 142,
        "chase_sr": 132, "vs_pace": 68, "vs_spin": 62, "form": 65,
        "econ": 7.5, "death_econ": 8.5, "wkts": 4, "bowling_type": "offspin",
    },
    "Pat Cummins": {
        "name": "Pat Cummins", "team": "srh", "hand": "R", "role": "allrounder",
        "avg": 14, "sr": 145, "powerplay_sr": 128, "death_sr": 170,
        "chase_sr": 150, "vs_pace": 40, "vs_spin": 35, "form": 82,
        "econ": 7.8, "death_econ": 8.5, "wkts": 12, "bowling_type": "pace",
    },
    "Bhuvneshwar Kumar": {
        "name": "Bhuvneshwar Kumar", "team": "srh", "hand": "R", "role": "bowl",
        "avg": 6, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 15, "vs_spin": 18, "form": 72,
        "econ": 7.2, "death_econ": 8.5, "wkts": 9, "bowling_type": "pace",
    },
    "Shahbaz Ahmed": {
        "name": "Shahbaz Ahmed", "team": "srh", "hand": "L", "role": "allrounder",
        "avg": 18, "sr": 132, "powerplay_sr": 125, "death_sr": 148,
        "chase_sr": 135, "vs_pace": 50, "vs_spin": 55, "form": 62,
        "econ": 7.8, "death_econ": 9.0, "wkts": 5, "bowling_type": "left-arm-spin",
    },
    "Rahul Tripathi": {
        "name": "Rahul Tripathi", "team": "srh", "hand": "R", "role": "bat",
        "avg": 28, "sr": 142, "powerplay_sr": 145, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 65, "vs_spin": 72, "form": 70,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Marco Jansen": {
        "name": "Marco Jansen", "team": "srh", "hand": "L", "role": "allrounder",
        "avg": 15, "sr": 138, "powerplay_sr": 128, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 38, "vs_spin": 42, "form": 75,
        "econ": 8.0, "death_econ": 9.0, "wkts": 10, "bowling_type": "pace",
    },
    "T Natarajan": {
        "name": "T Natarajan", "team": "srh", "hand": "L", "role": "bowl",
        "avg": 4, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 8, "vs_spin": 10, "form": 78,
        "econ": 7.5, "death_econ": 8.0, "wkts": 12, "bowling_type": "pace",
    },
    "Umran Malik": {
        "name": "Umran Malik", "team": "srh", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 75, "powerplay_sr": 60, "death_sr": 85,
        "chase_sr": 70, "vs_pace": 8, "vs_spin": 10, "form": 60,
        "econ": 9.0, "death_econ": 10.5, "wkts": 6, "bowling_type": "pace",
    },
    "Washington Sundar": {
        "name": "Washington Sundar", "team": "srh", "hand": "L", "role": "allrounder",
        "avg": 18, "sr": 125, "powerplay_sr": 120, "death_sr": 138,
        "chase_sr": 128, "vs_pace": 45, "vs_spin": 55, "form": 68,
        "econ": 6.8, "death_econ": 7.8, "wkts": 8, "bowling_type": "offspin",
    },
    "Abdul Samad": {
        "name": "Abdul Samad", "team": "srh", "hand": "R", "role": "bat",
        "avg": 20, "sr": 148, "powerplay_sr": 135, "death_sr": 172,
        "chase_sr": 150, "vs_pace": 62, "vs_spin": 55, "form": 58,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Glenn Phillips": {
        "name": "Glenn Phillips", "team": "srh", "hand": "R", "role": "wk-bat",
        "avg": 25, "sr": 152, "powerplay_sr": 145, "death_sr": 170,
        "chase_sr": 155, "vs_pace": 68, "vs_spin": 72, "form": 72,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Jaydev Unadkat": {
        "name": "Jaydev Unadkat", "team": "srh", "hand": "L", "role": "bowl",
        "avg": 6, "sr": 90, "powerplay_sr": 75, "death_sr": 100,
        "chase_sr": 85, "vs_pace": 12, "vs_spin": 15, "form": 62,
        "econ": 8.2, "death_econ": 9.5, "wkts": 7, "bowling_type": "pace",
    },

    # ── LSG ──────────────────────────────────────────────────────────
    "KL Rahul": {
        "name": "KL Rahul", "team": "lsg", "hand": "R", "role": "wk-bat",
        "avg": 45, "sr": 135, "powerplay_sr": 142, "death_sr": 148,
        "chase_sr": 138, "vs_pace": 80, "vs_spin": 75, "form": 84,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Quinton de Kock": {
        "name": "Quinton de Kock", "team": "lsg", "hand": "L", "role": "wk-bat",
        "avg": 35, "sr": 142, "powerplay_sr": 155, "death_sr": 150,
        "chase_sr": 145, "vs_pace": 78, "vs_spin": 68, "form": 80,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Nicholas Pooran": {
        "name": "Nicholas Pooran", "team": "lsg", "hand": "L", "role": "wk-bat",
        "avg": 25, "sr": 158, "powerplay_sr": 145, "death_sr": 188,
        "chase_sr": 162, "vs_pace": 72, "vs_spin": 65, "form": 76,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Marcus Stoinis": {
        "name": "Marcus Stoinis", "team": "lsg", "hand": "R", "role": "allrounder",
        "avg": 28, "sr": 148, "powerplay_sr": 142, "death_sr": 175,
        "chase_sr": 155, "vs_pace": 72, "vs_spin": 62, "form": 78,
        "econ": 8.5, "death_econ": 9.8, "wkts": 6, "bowling_type": "pace",
    },
    "Ayush Badoni": {
        "name": "Ayush Badoni", "team": "lsg", "hand": "R", "role": "bat",
        "avg": 26, "sr": 145, "powerplay_sr": 138, "death_sr": 165,
        "chase_sr": 148, "vs_pace": 65, "vs_spin": 72, "form": 74,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Krunal Pandya": {
        "name": "Krunal Pandya", "team": "lsg", "hand": "L", "role": "allrounder",
        "avg": 22, "sr": 130, "powerplay_sr": 125, "death_sr": 145,
        "chase_sr": 135, "vs_pace": 55, "vs_spin": 62, "form": 68,
        "econ": 7.2, "death_econ": 8.5, "wkts": 7, "bowling_type": "left-arm-spin",
    },
    "Deepak Hooda": {
        "name": "Deepak Hooda", "team": "lsg", "hand": "R", "role": "allrounder",
        "avg": 24, "sr": 138, "powerplay_sr": 132, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 62, "vs_spin": 58, "form": 65,
        "econ": 8.0, "death_econ": 9.2, "wkts": 4, "bowling_type": "offspin",
    },
    "Mark Wood": {
        "name": "Mark Wood", "team": "lsg", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 80,
        "econ": 7.8, "death_econ": 8.5, "wkts": 12, "bowling_type": "pace",
    },
    "Ravi Bishnoi": {
        "name": "Ravi Bishnoi", "team": "lsg", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 65, "powerplay_sr": 50, "death_sr": 75,
        "chase_sr": 60, "vs_pace": 8, "vs_spin": 10, "form": 82,
        "econ": 7.0, "death_econ": 8.0, "wkts": 14, "bowling_type": "legspin",
    },
    "Avesh Khan": {
        "name": "Avesh Khan", "team": "lsg", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 75, "powerplay_sr": 60, "death_sr": 85,
        "chase_sr": 70, "vs_pace": 10, "vs_spin": 12, "form": 68,
        "econ": 8.5, "death_econ": 9.8, "wkts": 8, "bowling_type": "pace",
    },
    "Mohsin Khan": {
        "name": "Mohsin Khan", "team": "lsg", "hand": "L", "role": "bowl",
        "avg": 4, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 8, "vs_spin": 10, "form": 72,
        "econ": 7.5, "death_econ": 8.5, "wkts": 10, "bowling_type": "pace",
    },
    "Naveen-ul-Haq": {
        "name": "Naveen-ul-Haq", "team": "lsg", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 78, "powerplay_sr": 62, "death_sr": 88,
        "chase_sr": 72, "vs_pace": 10, "vs_spin": 12, "form": 75,
        "econ": 7.8, "death_econ": 9.0, "wkts": 9, "bowling_type": "pace",
    },
    "Devdutt Padikkal": {
        "name": "Devdutt Padikkal", "team": "lsg", "hand": "L", "role": "bat",
        "avg": 28, "sr": 132, "powerplay_sr": 140, "death_sr": 142,
        "chase_sr": 135, "vs_pace": 68, "vs_spin": 62, "form": 62,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Manan Vohra": {
        "name": "Manan Vohra", "team": "lsg", "hand": "R", "role": "bat",
        "avg": 20, "sr": 130, "powerplay_sr": 138, "death_sr": 140,
        "chase_sr": 132, "vs_pace": 58, "vs_spin": 52, "form": 50,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Yash Thakur": {
        "name": "Yash Thakur", "team": "lsg", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 65,
        "econ": 8.2, "death_econ": 9.5, "wkts": 7, "bowling_type": "pace",
    },

    # ── DC ───────────────────────────────────────────────────────────
    "David Warner": {
        "name": "David Warner", "team": "dc", "hand": "L", "role": "bat",
        "avg": 42, "sr": 145, "powerplay_sr": 158, "death_sr": 155,
        "chase_sr": 148, "vs_pace": 82, "vs_spin": 72, "form": 78,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Jake Fraser-McGurk": {
        "name": "Jake Fraser-McGurk", "team": "dc", "hand": "R", "role": "bat",
        "avg": 22, "sr": 175, "powerplay_sr": 185, "death_sr": 180,
        "chase_sr": 170, "vs_pace": 72, "vs_spin": 55, "form": 82,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Rishabh Pant": {
        "name": "Rishabh Pant", "team": "dc", "hand": "L", "role": "wk-bat",
        "avg": 35, "sr": 150, "powerplay_sr": 145, "death_sr": 178,
        "chase_sr": 155, "vs_pace": 78, "vs_spin": 82, "form": 88,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Axar Patel": {
        "name": "Axar Patel", "team": "dc", "hand": "L", "role": "allrounder",
        "avg": 20, "sr": 138, "powerplay_sr": 128, "death_sr": 158,
        "chase_sr": 142, "vs_pace": 55, "vs_spin": 48, "form": 72,
        "econ": 7.0, "death_econ": 8.0, "wkts": 10, "bowling_type": "left-arm-spin",
    },
    "Tristan Stubbs": {
        "name": "Tristan Stubbs", "team": "dc", "hand": "R", "role": "bat",
        "avg": 22, "sr": 158, "powerplay_sr": 145, "death_sr": 185,
        "chase_sr": 162, "vs_pace": 70, "vs_spin": 65, "form": 76,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Prithvi Shaw": {
        "name": "Prithvi Shaw", "team": "dc", "hand": "R", "role": "bat",
        "avg": 24, "sr": 148, "powerplay_sr": 162, "death_sr": 145,
        "chase_sr": 145, "vs_pace": 72, "vs_spin": 58, "form": 55,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Abishek Porel": {
        "name": "Abishek Porel", "team": "dc", "hand": "L", "role": "wk-bat",
        "avg": 20, "sr": 135, "powerplay_sr": 140, "death_sr": 148,
        "chase_sr": 138, "vs_pace": 60, "vs_spin": 58, "form": 62,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Kuldeep Yadav": {
        "name": "Kuldeep Yadav", "team": "dc", "hand": "L", "role": "bowl",
        "avg": 6, "sr": 85, "powerplay_sr": 72, "death_sr": 95,
        "chase_sr": 80, "vs_pace": 12, "vs_spin": 15, "form": 85,
        "econ": 7.0, "death_econ": 8.2, "wkts": 14, "bowling_type": "left-arm-spin",
    },
    "Khaleel Ahmed": {
        "name": "Khaleel Ahmed", "team": "dc", "hand": "L", "role": "bowl",
        "avg": 5, "sr": 75, "powerplay_sr": 60, "death_sr": 85,
        "chase_sr": 70, "vs_pace": 8, "vs_spin": 10, "form": 72,
        "econ": 8.0, "death_econ": 9.2, "wkts": 9, "bowling_type": "pace",
    },
    "Ishant Sharma": {
        "name": "Ishant Sharma", "team": "dc", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 8, "vs_spin": 10, "form": 58,
        "econ": 8.5, "death_econ": 9.8, "wkts": 6, "bowling_type": "pace",
    },
    "Mitchell Marsh": {
        "name": "Mitchell Marsh", "team": "dc", "hand": "R", "role": "allrounder",
        "avg": 30, "sr": 148, "powerplay_sr": 142, "death_sr": 165,
        "chase_sr": 152, "vs_pace": 75, "vs_spin": 65, "form": 78,
        "econ": 8.5, "death_econ": 9.5, "wkts": 5, "bowling_type": "pace",
    },
    "Mukesh Kumar": {
        "name": "Mukesh Kumar", "team": "dc", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 78, "powerplay_sr": 62, "death_sr": 88,
        "chase_sr": 72, "vs_pace": 10, "vs_spin": 12, "form": 70,
        "econ": 8.0, "death_econ": 9.2, "wkts": 8, "bowling_type": "pace",
    },
    "Rasikh Salam": {
        "name": "Rasikh Salam", "team": "dc", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 72, "powerplay_sr": 58, "death_sr": 82,
        "chase_sr": 68, "vs_pace": 8, "vs_spin": 10, "form": 65,
        "econ": 8.5, "death_econ": 9.8, "wkts": 6, "bowling_type": "pace",
    },
    "Sumit Kumar": {
        "name": "Sumit Kumar", "team": "dc", "hand": "R", "role": "allrounder",
        "avg": 12, "sr": 130, "powerplay_sr": 120, "death_sr": 148,
        "chase_sr": 132, "vs_pace": 40, "vs_spin": 38, "form": 52,
        "econ": 8.8, "death_econ": 10.0, "wkts": 3, "bowling_type": "pace",
    },

    # ── RR ───────────────────────────────────────────────────────────
    "Sanju Samson": {
        "name": "Sanju Samson", "team": "rr", "hand": "R", "role": "wk-bat",
        "avg": 32, "sr": 148, "powerplay_sr": 155, "death_sr": 168,
        "chase_sr": 152, "vs_pace": 75, "vs_spin": 72, "form": 85,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Yashasvi Jaiswal": {
        "name": "Yashasvi Jaiswal", "team": "rr", "hand": "L", "role": "bat",
        "avg": 38, "sr": 158, "powerplay_sr": 170, "death_sr": 165,
        "chase_sr": 155, "vs_pace": 80, "vs_spin": 75, "form": 92,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Jos Buttler": {
        "name": "Jos Buttler", "team": "rr", "hand": "R", "role": "wk-bat",
        "avg": 40, "sr": 155, "powerplay_sr": 162, "death_sr": 175,
        "chase_sr": 160, "vs_pace": 82, "vs_spin": 75, "form": 80,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Shimron Hetmyer": {
        "name": "Shimron Hetmyer", "team": "rr", "hand": "L", "role": "bat",
        "avg": 24, "sr": 158, "powerplay_sr": 142, "death_sr": 190,
        "chase_sr": 162, "vs_pace": 70, "vs_spin": 72, "form": 72,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Dhruv Jurel": {
        "name": "Dhruv Jurel", "team": "rr", "hand": "R", "role": "wk-bat",
        "avg": 22, "sr": 138, "powerplay_sr": 132, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 62, "vs_spin": 58, "form": 68,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Riyan Parag": {
        "name": "Riyan Parag", "team": "rr", "hand": "R", "role": "allrounder",
        "avg": 24, "sr": 140, "powerplay_sr": 132, "death_sr": 162,
        "chase_sr": 145, "vs_pace": 65, "vs_spin": 60, "form": 75,
        "econ": 8.5, "death_econ": 9.8, "wkts": 3, "bowling_type": "legspin",
    },
    "Ravichandran Ashwin": {
        "name": "Ravichandran Ashwin", "team": "rr", "hand": "R", "role": "bowl",
        "avg": 12, "sr": 115, "powerplay_sr": 105, "death_sr": 128,
        "chase_sr": 118, "vs_pace": 35, "vs_spin": 45, "form": 70,
        "econ": 6.8, "death_econ": 7.8, "wkts": 10, "bowling_type": "offspin",
    },
    "Yuzvendra Chahal": {
        "name": "Yuzvendra Chahal", "team": "rr", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 65, "powerplay_sr": 50, "death_sr": 75,
        "chase_sr": 60, "vs_pace": 8, "vs_spin": 10, "form": 78,
        "econ": 7.2, "death_econ": 8.5, "wkts": 14, "bowling_type": "legspin",
    },
    "Sandeep Sharma": {
        "name": "Sandeep Sharma", "team": "rr", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 78, "powerplay_sr": 62, "death_sr": 88,
        "chase_sr": 72, "vs_pace": 10, "vs_spin": 12, "form": 62,
        "econ": 7.8, "death_econ": 9.0, "wkts": 8, "bowling_type": "pace",
    },
    "Donovan Ferreira": {
        "name": "Donovan Ferreira", "team": "rr", "hand": "R", "role": "bat",
        "avg": 20, "sr": 142, "powerplay_sr": 135, "death_sr": 158,
        "chase_sr": 145, "vs_pace": 60, "vs_spin": 55, "form": 58,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Kunal Rathore": {
        "name": "Kunal Rathore", "team": "rr", "hand": "R", "role": "bat",
        "avg": 16, "sr": 128, "powerplay_sr": 125, "death_sr": 140,
        "chase_sr": 130, "vs_pace": 50, "vs_spin": 48, "form": 48,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Nandre Burger": {
        "name": "Nandre Burger", "team": "rr", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 70,
        "econ": 8.2, "death_econ": 9.5, "wkts": 8, "bowling_type": "pace",
    },
    "Tom Kohler-Cadmore": {
        "name": "Tom Kohler-Cadmore", "team": "rr", "hand": "R", "role": "wk-bat",
        "avg": 22, "sr": 135, "powerplay_sr": 140, "death_sr": 148,
        "chase_sr": 138, "vs_pace": 65, "vs_spin": 58, "form": 55,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },

    # ── PBKS ─────────────────────────────────────────────────────────
    "Shikhar Dhawan": {
        "name": "Shikhar Dhawan", "team": "pbks", "hand": "L", "role": "bat",
        "avg": 38, "sr": 132, "powerplay_sr": 142, "death_sr": 140,
        "chase_sr": 135, "vs_pace": 78, "vs_spin": 72, "form": 65,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Jonny Bairstow": {
        "name": "Jonny Bairstow", "team": "pbks", "hand": "R", "role": "wk-bat",
        "avg": 30, "sr": 148, "powerplay_sr": 158, "death_sr": 162,
        "chase_sr": 150, "vs_pace": 78, "vs_spin": 65, "form": 72,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Liam Livingstone": {
        "name": "Liam Livingstone", "team": "pbks", "hand": "R", "role": "allrounder",
        "avg": 26, "sr": 158, "powerplay_sr": 150, "death_sr": 185,
        "chase_sr": 162, "vs_pace": 72, "vs_spin": 68, "form": 78,
        "econ": 8.0, "death_econ": 9.0, "wkts": 5, "bowling_type": "legspin",
    },
    "Sam Curran": {
        "name": "Sam Curran", "team": "pbks", "hand": "L", "role": "allrounder",
        "avg": 22, "sr": 142, "powerplay_sr": 135, "death_sr": 165,
        "chase_sr": 148, "vs_pace": 60, "vs_spin": 55, "form": 75,
        "econ": 8.0, "death_econ": 9.0, "wkts": 10, "bowling_type": "pace",
    },
    "Jitesh Sharma": {
        "name": "Jitesh Sharma", "team": "pbks", "hand": "R", "role": "wk-bat",
        "avg": 22, "sr": 155, "powerplay_sr": 140, "death_sr": 180,
        "chase_sr": 158, "vs_pace": 65, "vs_spin": 60, "form": 72,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Shahrukh Khan": {
        "name": "Shahrukh Khan", "team": "pbks", "hand": "R", "role": "bat",
        "avg": 20, "sr": 148, "powerplay_sr": 132, "death_sr": 178,
        "chase_sr": 155, "vs_pace": 68, "vs_spin": 55, "form": 65,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Harpreet Brar": {
        "name": "Harpreet Brar", "team": "pbks", "hand": "L", "role": "allrounder",
        "avg": 14, "sr": 125, "powerplay_sr": 118, "death_sr": 140,
        "chase_sr": 128, "vs_pace": 38, "vs_spin": 42, "form": 68,
        "econ": 7.2, "death_econ": 8.5, "wkts": 8, "bowling_type": "left-arm-spin",
    },
    "Arshdeep Singh": {
        "name": "Arshdeep Singh", "team": "pbks", "hand": "L", "role": "bowl",
        "avg": 4, "sr": 70, "powerplay_sr": 55, "death_sr": 80,
        "chase_sr": 65, "vs_pace": 8, "vs_spin": 10, "form": 85,
        "econ": 7.5, "death_econ": 7.8, "wkts": 14, "bowling_type": "pace",
    },
    "Kagiso Rabada": {
        "name": "Kagiso Rabada", "team": "pbks", "hand": "R", "role": "bowl",
        "avg": 6, "sr": 85, "powerplay_sr": 70, "death_sr": 95,
        "chase_sr": 80, "vs_pace": 12, "vs_spin": 15, "form": 82,
        "econ": 7.8, "death_econ": 8.5, "wkts": 12, "bowling_type": "pace",
    },
    "Rahul Chahar": {
        "name": "Rahul Chahar", "team": "pbks", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 68, "powerplay_sr": 55, "death_sr": 78,
        "chase_sr": 62, "vs_pace": 8, "vs_spin": 10, "form": 72,
        "econ": 7.5, "death_econ": 8.8, "wkts": 10, "bowling_type": "legspin",
    },
    "Nathan Ellis": {
        "name": "Nathan Ellis", "team": "pbks", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 82, "powerplay_sr": 68, "death_sr": 92,
        "chase_sr": 78, "vs_pace": 10, "vs_spin": 12, "form": 75,
        "econ": 8.0, "death_econ": 8.8, "wkts": 9, "bowling_type": "pace",
    },
    "Atharva Taide": {
        "name": "Atharva Taide", "team": "pbks", "hand": "L", "role": "bat",
        "avg": 18, "sr": 130, "powerplay_sr": 135, "death_sr": 142,
        "chase_sr": 132, "vs_pace": 55, "vs_spin": 50, "form": 52,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Prabhsimran Singh": {
        "name": "Prabhsimran Singh", "team": "pbks", "hand": "R", "role": "wk-bat",
        "avg": 20, "sr": 145, "powerplay_sr": 155, "death_sr": 150,
        "chase_sr": 142, "vs_pace": 65, "vs_spin": 55, "form": 58,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Vidwath Kaverappa": {
        "name": "Vidwath Kaverappa", "team": "pbks", "hand": "R", "role": "bowl",
        "avg": 4, "sr": 72, "powerplay_sr": 58, "death_sr": 82,
        "chase_sr": 68, "vs_pace": 8, "vs_spin": 10, "form": 62,
        "econ": 8.5, "death_econ": 9.8, "wkts": 5, "bowling_type": "pace",
    },
    "Rishi Dhawan": {
        "name": "Rishi Dhawan", "team": "pbks", "hand": "R", "role": "allrounder",
        "avg": 16, "sr": 135, "powerplay_sr": 125, "death_sr": 155,
        "chase_sr": 138, "vs_pace": 45, "vs_spin": 40, "form": 55,
        "econ": 8.5, "death_econ": 9.5, "wkts": 5, "bowling_type": "pace",
    },

    # ── GT ───────────────────────────────────────────────────────────
    "Shubman Gill": {
        "name": "Shubman Gill", "team": "gt", "hand": "R", "role": "bat",
        "avg": 42, "sr": 140, "powerplay_sr": 148, "death_sr": 155,
        "chase_sr": 142, "vs_pace": 80, "vs_spin": 78, "form": 88,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Wriddhiman Saha": {
        "name": "Wriddhiman Saha", "team": "gt", "hand": "R", "role": "wk-bat",
        "avg": 25, "sr": 128, "powerplay_sr": 135, "death_sr": 138,
        "chase_sr": 130, "vs_pace": 65, "vs_spin": 68, "form": 58,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Sai Sudharsan": {
        "name": "Sai Sudharsan", "team": "gt", "hand": "L", "role": "bat",
        "avg": 35, "sr": 138, "powerplay_sr": 142, "death_sr": 152,
        "chase_sr": 140, "vs_pace": 72, "vs_spin": 75, "form": 82,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "David Miller": {
        "name": "David Miller", "team": "gt", "hand": "L", "role": "bat",
        "avg": 30, "sr": 148, "powerplay_sr": 132, "death_sr": 185,
        "chase_sr": 155, "vs_pace": 72, "vs_spin": 68, "form": 75,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Rashid Khan": {
        "name": "Rashid Khan", "team": "gt", "hand": "R", "role": "bowl",
        "avg": 12, "sr": 145, "powerplay_sr": 130, "death_sr": 168,
        "chase_sr": 150, "vs_pace": 42, "vs_spin": 48, "form": 90,
        "econ": 6.2, "death_econ": 7.0, "wkts": 16, "bowling_type": "legspin",
    },
    "Rahul Tewatia": {
        "name": "Rahul Tewatia", "team": "gt", "hand": "L", "role": "allrounder",
        "avg": 20, "sr": 142, "powerplay_sr": 128, "death_sr": 172,
        "chase_sr": 150, "vs_pace": 60, "vs_spin": 55, "form": 68,
        "econ": 7.8, "death_econ": 9.0, "wkts": 5, "bowling_type": "legspin",
    },
    "Vijay Shankar": {
        "name": "Vijay Shankar", "team": "gt", "hand": "R", "role": "allrounder",
        "avg": 20, "sr": 128, "powerplay_sr": 122, "death_sr": 142,
        "chase_sr": 130, "vs_pace": 58, "vs_spin": 55, "form": 60,
        "econ": 8.5, "death_econ": 9.8, "wkts": 4, "bowling_type": "medium",
    },
    "Mohammed Shami": {
        "name": "Mohammed Shami", "team": "gt", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 80, "powerplay_sr": 65, "death_sr": 90,
        "chase_sr": 75, "vs_pace": 10, "vs_spin": 12, "form": 78,
        "econ": 7.5, "death_econ": 8.5, "wkts": 12, "bowling_type": "pace",
    },
    "Josh Little": {
        "name": "Josh Little", "team": "gt", "hand": "L", "role": "bowl",
        "avg": 5, "sr": 82, "powerplay_sr": 68, "death_sr": 92,
        "chase_sr": 78, "vs_pace": 10, "vs_spin": 12, "form": 72,
        "econ": 8.0, "death_econ": 9.0, "wkts": 8, "bowling_type": "pace",
    },
    "Noor Ahmad": {
        "name": "Noor Ahmad", "team": "gt", "hand": "L", "role": "bowl",
        "avg": 4, "sr": 68, "powerplay_sr": 55, "death_sr": 78,
        "chase_sr": 62, "vs_pace": 8, "vs_spin": 10, "form": 78,
        "econ": 7.0, "death_econ": 8.0, "wkts": 12, "bowling_type": "left-arm-spin",
    },
    "Umesh Yadav": {
        "name": "Umesh Yadav", "team": "gt", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 78, "powerplay_sr": 62, "death_sr": 88,
        "chase_sr": 72, "vs_pace": 10, "vs_spin": 12, "form": 60,
        "econ": 8.5, "death_econ": 10.0, "wkts": 6, "bowling_type": "pace",
    },
    "Kane Williamson": {
        "name": "Kane Williamson", "team": "gt", "hand": "R", "role": "bat",
        "avg": 38, "sr": 122, "powerplay_sr": 118, "death_sr": 132,
        "chase_sr": 125, "vs_pace": 78, "vs_spin": 80, "form": 62,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Matthew Wade": {
        "name": "Matthew Wade", "team": "gt", "hand": "L", "role": "wk-bat",
        "avg": 22, "sr": 145, "powerplay_sr": 152, "death_sr": 158,
        "chase_sr": 148, "vs_pace": 68, "vs_spin": 62, "form": 60,
        "econ": None, "death_econ": None, "wkts": None, "bowling_type": None,
    },
    "Azmatullah Omarzai": {
        "name": "Azmatullah Omarzai", "team": "gt", "hand": "R", "role": "allrounder",
        "avg": 18, "sr": 138, "powerplay_sr": 130, "death_sr": 155,
        "chase_sr": 140, "vs_pace": 55, "vs_spin": 50, "form": 70,
        "econ": 8.2, "death_econ": 9.5, "wkts": 6, "bowling_type": "pace",
    },
    "Mohit Sharma": {
        "name": "Mohit Sharma", "team": "gt", "hand": "R", "role": "bowl",
        "avg": 5, "sr": 78, "powerplay_sr": 62, "death_sr": 88,
        "chase_sr": 72, "vs_pace": 10, "vs_spin": 12, "form": 72,
        "econ": 7.8, "death_econ": 8.8, "wkts": 10, "bowling_type": "pace",
    },
}


def get_profile(name: str) -> dict | None:
    """
    Return the full profile dict for a player by exact canonical name.

    Parameters
    ----------
    name : str   e.g. "Virat Kohli"

    Returns
    -------
    dict | None
    """
    return PLAYER_PROFILES.get(name)


def get_team_profiles(team_id: str) -> list[dict]:
    """
    Return all player profiles belonging to a team.

    Parameters
    ----------
    team_id : str   e.g. "rcb"

    Returns
    -------
    list[dict]
    """
    return [p for p in PLAYER_PROFILES.values() if p["team"] == team_id]


def get_all_names() -> list[str]:
    """Return a list of all canonical player names."""
    return list(PLAYER_PROFILES.keys())
