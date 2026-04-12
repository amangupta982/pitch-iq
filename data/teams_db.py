"""
data/teams_db.py
----------------
IPL 2026 squads with rich player profiles for coaching analytics.
Each batter has: avg, sr, death_sr, chase_sr, form, hand
Each bowler has: econ, death_econ, wkts, form, type
"""

TEAMS = {
    "rcb": {
        "name": "Royal Challengers Bengaluru", "short": "RCB", "color": "#E25822",
        "home": "Chinnaswamy, Bengaluru", "avg_score": 178, "chase_win": 0.54,
        "batters": [
            {"name": "Virat Kohli",    "avg": 52, "sr": 138, "death_sr": 145, "chase_sr": 142, "form": 92, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Faf du Plessis", "avg": 38, "sr": 145, "death_sr": 155, "chase_sr": 148, "form": 74, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Glenn Maxwell",  "avg": 29, "sr": 175, "death_sr": 195, "chase_sr": 178, "form": 65, "hand": "R", "role": "allrounder", "lower_order_score": 30},
            {"name": "Rajat Patidar",  "avg": 34, "sr": 148, "death_sr": 165, "chase_sr": 150, "form": 70, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Dinesh Karthik", "avg": 22, "sr": 168, "death_sr": 190, "chase_sr": 172, "form": 62, "hand": "R", "role": "wk-bat", "lower_order_score": 60},
            {"name": "Suyash Prabhudessai", "avg": 18, "sr": 140, "death_sr": 155, "chase_sr": 140, "form": 55, "hand": "R", "role": "bat", "lower_order_score": 20},
        ],
        "bowlers": [
            {"name": "Mohammed Siraj",    "econ": 7.8,  "death_econ": 9.2,  "wkts": 18, "form": 80, "type": "pace"},
            {"name": "Yuzvendra Chahal",  "econ": 8.2,  "death_econ": 10.5, "wkts": 15, "form": 72, "type": "leg-spin"},
            {"name": "Alzarri Joseph",    "econ": 8.9,  "death_econ": 9.8,  "wkts": 12, "form": 65, "type": "pace"},
            {"name": "Glenn Maxwell",     "econ": 9.0,  "death_econ": 10.0, "wkts": 5,  "form": 55, "type": "off-spin"},
            {"name": "Karn Sharma",       "econ": 8.5,  "death_econ": 10.2, "wkts": 8,  "form": 60, "type": "leg-spin"},
        ],
        "squad": [
            {"name": "Will Jacks",      "role": "allrounder", "form": 70},
            {"name": "Mahipal Lomror",  "role": "bat",        "form": 58},
            {"name": "Reece Topley",    "role": "bowl",       "form": 64},
        ],
    },
    "csk": {
        "name": "Chennai Super Kings", "short": "CSK", "color": "#F5A623",
        "home": "Chepauk, Chennai", "avg_score": 172, "chase_win": 0.58,
        "batters": [
            {"name": "Ruturaj Gaikwad", "avg": 45, "sr": 135, "death_sr": 148, "chase_sr": 138, "form": 85, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Devon Conway",    "avg": 40, "sr": 128, "death_sr": 140, "chase_sr": 132, "form": 78, "hand": "L", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Ajinkya Rahane",  "avg": 32, "sr": 122, "death_sr": 135, "chase_sr": 128, "form": 65, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Shivam Dube",     "avg": 32, "sr": 158, "death_sr": 175, "chase_sr": 162, "form": 73, "hand": "L", "role": "allrounder", "lower_order_score": 40},
            {"name": "MS Dhoni",        "avg": 25, "sr": 162, "death_sr": 190, "chase_sr": 172, "form": 60, "hand": "R", "role": "wk-bat", "lower_order_score": 80},
            {"name": "Ravindra Jadeja", "avg": 28, "sr": 142, "death_sr": 155, "chase_sr": 145, "form": 76, "hand": "L", "role": "allrounder", "lower_order_score": 60},
        ],
        "bowlers": [
            {"name": "Deepak Chahar",       "econ": 7.5, "death_econ": 9.0,  "wkts": 14, "form": 76, "type": "swing"},
            {"name": "Ravindra Jadeja",     "econ": 7.1, "death_econ": 9.5,  "wkts": 11, "form": 82, "type": "spin"},
            {"name": "Matheesha Pathirana", "econ": 8.4, "death_econ": 8.8,  "wkts": 16, "form": 70, "type": "pace"},
            {"name": "Tushar Deshpande",    "econ": 8.8, "death_econ": 9.2,  "wkts": 9,  "form": 62, "type": "pace"},
            {"name": "Maheesh Theekshana",  "econ": 7.9, "death_econ": 9.8,  "wkts": 12, "form": 68, "type": "off-spin"},
        ],
        "squad": [
            {"name": "Ambati Rayudu",  "role": "bat",        "form": 60},
            {"name": "Ben Stokes",     "role": "allrounder", "form": 72},
            {"name": "Simarjeet Singh","role": "bowl",       "form": 55},
        ],
    },
    "mi": {
        "name": "Mumbai Indians", "short": "MI", "color": "#1B6BB0",
        "home": "Wankhede, Mumbai", "avg_score": 181, "chase_win": 0.52,
        "batters": [
            {"name": "Rohit Sharma",        "avg": 42, "sr": 142, "death_sr": 158, "chase_sr": 146, "form": 80, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Ishan Kishan",        "avg": 35, "sr": 155, "death_sr": 168, "chase_sr": 158, "form": 68, "hand": "L", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Suryakumar Yadav",    "avg": 38, "sr": 178, "death_sr": 205, "chase_sr": 182, "form": 88, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Tilak Varma",         "avg": 35, "sr": 148, "death_sr": 162, "chase_sr": 152, "form": 78, "hand": "L", "role": "bat", "lower_order_score": 0},
            {"name": "Tim David",           "avg": 28, "sr": 168, "death_sr": 192, "chase_sr": 172, "form": 72, "hand": "R", "role": "bat", "lower_order_score": 50},
            {"name": "Hardik Pandya",       "avg": 30, "sr": 152, "death_sr": 175, "chase_sr": 156, "form": 74, "hand": "R", "role": "allrounder", "lower_order_score": 60},
        ],
        "bowlers": [
            {"name": "Jasprit Bumrah",  "econ": 6.9,  "death_econ": 7.8,  "wkts": 22, "form": 95, "type": "pace"},
            {"name": "Hardik Pandya",   "econ": 8.5,  "death_econ": 9.5,  "wkts": 10, "form": 68, "type": "fast-medium"},
            {"name": "Piyush Chawla",   "econ": 8.0,  "death_econ": 9.8,  "wkts": 10, "form": 62, "type": "leg-spin"},
            {"name": "Gerald Coetzee",  "econ": 9.1,  "death_econ": 9.8,  "wkts": 13, "form": 66, "type": "pace"},
            {"name": "Akash Madhwal",   "econ": 8.3,  "death_econ": 8.9,  "wkts": 11, "form": 64, "type": "pace"},
        ],
        "squad": [
            {"name": "Dewald Brevis",   "role": "bat",        "form": 72},
            {"name": "Ramandeep Singh", "role": "allrounder", "form": 60},
            {"name": "Jason Behrendorff","role": "bowl",      "form": 66},
        ],
    },
    "kkr": {
        "name": "Kolkata Knight Riders", "short": "KKR", "color": "#6F4BA8",
        "home": "Eden Gardens, Kolkata", "avg_score": 176, "chase_win": 0.55,
        "batters": [
            {"name": "Phil Salt",    "avg": 36, "sr": 160, "death_sr": 175, "chase_sr": 164, "form": 76, "hand": "R", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Sunil Narine", "avg": 27, "sr": 170, "death_sr": 180, "chase_sr": 172, "form": 72, "hand": "L", "role": "allrounder", "lower_order_score": 40},
            {"name": "Shreyas Iyer", "avg": 43, "sr": 132, "death_sr": 148, "chase_sr": 136, "form": 82, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "Rinku Singh",  "avg": 30, "sr": 152, "death_sr": 180, "chase_sr": 156, "form": 78, "hand": "L", "role": "bat", "lower_order_score": 50},
            {"name": "Andre Russell","avg": 25, "sr": 175, "death_sr": 200, "chase_sr": 180, "form": 74, "hand": "R", "role": "allrounder", "lower_order_score": 80},
            {"name": "Venkatesh Iyer","avg": 28, "sr": 145, "death_sr": 162, "chase_sr": 148, "form": 70, "hand": "L", "role": "allrounder", "lower_order_score": 30},
        ],
        "bowlers": [
            {"name": "Varun Chakravarthy", "econ": 7.4, "death_econ": 9.5,  "wkts": 17, "form": 80, "type": "spin"},
            {"name": "Mitchell Starc",     "econ": 8.8, "death_econ": 9.0,  "wkts": 14, "form": 70, "type": "pace"},
            {"name": "Harshit Rana",       "econ": 8.6, "death_econ": 9.4,  "wkts": 12, "form": 65, "type": "pace"},
            {"name": "Sunil Narine",       "econ": 7.6, "death_econ": 9.8,  "wkts": 8,  "form": 68, "type": "off-spin"},
            {"name": "Andre Russell",      "econ": 9.2, "death_econ": 9.6,  "wkts": 7,  "form": 65, "type": "fast-medium"},
        ],
        "squad": [
            {"name": "Manish Pandey",  "role": "bat",        "form": 60},
            {"name": "Lockie Ferguson","role": "bowl",       "form": 70},
            {"name": "Angkrish Raghuvanshi","role": "bat",   "form": 65},
        ],
    },
    "srh": {
        "name": "Sunrisers Hyderabad", "short": "SRH", "color": "#F26522",
        "home": "Rajiv Gandhi, Hyderabad", "avg_score": 186, "chase_win": 0.50,
        "batters": [
            {"name": "Travis Head",      "avg": 38, "sr": 175, "death_sr": 192, "chase_sr": 178, "form": 84, "hand": "L", "role": "bat", "lower_order_score": 0},
            {"name": "Abhishek Sharma",  "avg": 30, "sr": 180, "death_sr": 195, "chase_sr": 182, "form": 78, "hand": "L", "role": "bat", "lower_order_score": 0},
            {"name": "Heinrich Klaasen", "avg": 42, "sr": 162, "death_sr": 185, "chase_sr": 165, "form": 88, "hand": "R", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Aiden Markram",    "avg": 35, "sr": 145, "death_sr": 158, "chase_sr": 148, "form": 72, "hand": "R", "role": "allrounder", "lower_order_score": 20},
            {"name": "Nitish Reddy",     "avg": 28, "sr": 148, "death_sr": 168, "chase_sr": 152, "form": 74, "hand": "R", "role": "allrounder", "lower_order_score": 55},
            {"name": "Abdul Samad",      "avg": 20, "sr": 155, "death_sr": 178, "chase_sr": 158, "form": 66, "hand": "R", "role": "bat", "lower_order_score": 65},
        ],
        "bowlers": [
            {"name": "Pat Cummins",       "econ": 8.1, "death_econ": 8.6,  "wkts": 16, "form": 80, "type": "pace"},
            {"name": "Bhuvneshwar Kumar", "econ": 7.6, "death_econ": 8.4,  "wkts": 13, "form": 72, "type": "swing"},
            {"name": "Mayank Markande",   "econ": 8.4, "death_econ": 10.2, "wkts": 10, "form": 62, "type": "leg-spin"},
            {"name": "T Natarajan",       "econ": 8.2, "death_econ": 8.5,  "wkts": 11, "form": 70, "type": "pace"},
            {"name": "Jaydev Unadkat",    "econ": 8.6, "death_econ": 9.0,  "wkts": 8,  "form": 62, "type": "fast-medium"},
        ],
        "squad": [
            {"name": "Glenn Phillips",   "role": "allrounder", "form": 70},
            {"name": "Shahbaz Ahmed",    "role": "allrounder", "form": 62},
            {"name": "Umran Malik",      "role": "bowl",       "form": 68},
        ],
    },
    "lsg": {
        "name": "Lucknow Super Giants", "short": "LSG", "color": "#00A868",
        "home": "BRSABV Ekana, Lucknow", "avg_score": 173, "chase_win": 0.54,
        "batters": [
            {"name": "KL Rahul",        "avg": 46, "sr": 136, "death_sr": 150, "chase_sr": 140, "form": 82, "hand": "R", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Quinton de Kock", "avg": 38, "sr": 148, "death_sr": 162, "chase_sr": 152, "form": 76, "hand": "L", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Marcus Stoinis",  "avg": 30, "sr": 155, "death_sr": 170, "chase_sr": 158, "form": 70, "hand": "R", "role": "allrounder", "lower_order_score": 50},
            {"name": "Nicholas Pooran", "avg": 34, "sr": 162, "death_sr": 188, "chase_sr": 165, "form": 74, "hand": "L", "role": "wk-bat", "lower_order_score": 40},
            {"name": "Ayush Badoni",    "avg": 26, "sr": 145, "death_sr": 162, "chase_sr": 148, "form": 68, "hand": "R", "role": "bat", "lower_order_score": 30},
            {"name": "Deepak Hooda",    "avg": 24, "sr": 138, "death_sr": 155, "chase_sr": 142, "form": 64, "hand": "R", "role": "allrounder", "lower_order_score": 40},
        ],
        "bowlers": [
            {"name": "Ravi Bishnoi", "econ": 7.5, "death_econ": 9.6,  "wkts": 16, "form": 80, "type": "leg-spin"},
            {"name": "Avesh Khan",   "econ": 8.7, "death_econ": 9.2,  "wkts": 12, "form": 65, "type": "pace"},
            {"name": "Mark Wood",    "econ": 8.9, "death_econ": 9.4,  "wkts": 14, "form": 68, "type": "pace"},
            {"name": "Krunal Pandya","econ": 7.8, "death_econ": 9.8,  "wkts": 8,  "form": 66, "type": "spin"},
            {"name": "Mohsin Khan",  "econ": 8.1, "death_econ": 8.8,  "wkts": 10, "form": 64, "type": "fast-medium"},
        ],
        "squad": [
            {"name": "Prerak Mankad",    "role": "allrounder", "form": 60},
            {"name": "Karan Sharma",     "role": "bowl",       "form": 58},
            {"name": "Manimaran Siddharth","role": "bowl",     "form": 62},
        ],
    },
    "dc": {
        "name": "Delhi Capitals", "short": "DC", "color": "#0B3D91",
        "home": "Arun Jaitley, Delhi", "avg_score": 174, "chase_win": 0.53,
        "batters": [
            {"name": "Jake Fraser-McGurk", "avg": 32, "sr": 172, "death_sr": 188, "chase_sr": 175, "form": 80, "hand": "R", "role": "bat", "lower_order_score": 0},
            {"name": "David Warner",       "avg": 41, "sr": 148, "death_sr": 162, "chase_sr": 152, "form": 75, "hand": "L", "role": "bat", "lower_order_score": 0},
            {"name": "Axar Patel",         "avg": 26, "sr": 145, "death_sr": 162, "chase_sr": 148, "form": 68, "hand": "L", "role": "allrounder", "lower_order_score": 55},
            {"name": "Tristan Stubbs",     "avg": 28, "sr": 155, "death_sr": 178, "chase_sr": 158, "form": 66, "hand": "R", "role": "bat", "lower_order_score": 45},
            {"name": "Rishabh Pant",       "avg": 34, "sr": 148, "death_sr": 168, "chase_sr": 152, "form": 76, "hand": "L", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Lalit Yadav",        "avg": 20, "sr": 138, "death_sr": 155, "chase_sr": 142, "form": 62, "hand": "R", "role": "allrounder", "lower_order_score": 40},
        ],
        "bowlers": [
            {"name": "Kuldeep Yadav",  "econ": 7.6, "death_econ": 9.8,  "wkts": 19, "form": 85, "type": "spin"},
            {"name": "Anrich Nortje",  "econ": 7.9, "death_econ": 8.5,  "wkts": 15, "form": 78, "type": "pace"},
            {"name": "Axar Patel",     "econ": 7.8, "death_econ": 9.5,  "wkts": 10, "form": 70, "type": "spin"},
            {"name": "Mukesh Kumar",   "econ": 8.8, "death_econ": 9.2,  "wkts": 10, "form": 64, "type": "pace"},
            {"name": "Ishant Sharma",  "econ": 8.5, "death_econ": 9.0,  "wkts": 9,  "form": 55, "type": "pace"},
        ],
        "squad": [
            {"name": "Yash Dhull",        "role": "bat",        "form": 60},
            {"name": "Khaleel Ahmed",     "role": "bowl",       "form": 62},
            {"name": "Priyam Garg",       "role": "bat",        "form": 58},
        ],
    },
    "rr": {
        "name": "Rajasthan Royals", "short": "RR", "color": "#C0437A",
        "home": "Sawai Mansingh, Jaipur", "avg_score": 177, "chase_win": 0.56,
        "batters": [
            {"name": "Jos Buttler",       "avg": 48, "sr": 152, "death_sr": 172, "chase_sr": 156, "form": 86, "hand": "R", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Yashasvi Jaiswal",  "avg": 44, "sr": 162, "death_sr": 175, "chase_sr": 165, "form": 90, "hand": "L", "role": "bat", "lower_order_score": 0},
            {"name": "Sanju Samson",      "avg": 36, "sr": 145, "death_sr": 162, "chase_sr": 148, "form": 74, "hand": "R", "role": "wk-bat", "lower_order_score": 0},
            {"name": "Shimron Hetmyer",   "avg": 27, "sr": 165, "death_sr": 192, "chase_sr": 168, "form": 70, "hand": "L", "role": "bat", "lower_order_score": 50},
            {"name": "Dhruv Jurel",       "avg": 24, "sr": 138, "death_sr": 155, "chase_sr": 142, "form": 66, "hand": "R", "role": "wk-bat", "lower_order_score": 40},
            {"name": "Rovman Powell",     "avg": 22, "sr": 158, "death_sr": 180, "chase_sr": 162, "form": 68, "hand": "R", "role": "bat", "lower_order_score": 60},
        ],
        "bowlers": [
            {"name": "Trent Boult",           "econ": 7.2, "death_econ": 8.2,  "wkts": 18, "form": 82, "type": "swing"},
            {"name": "Yuzvendra Chahal",      "econ": 8.0, "death_econ": 10.2, "wkts": 16, "form": 75, "type": "leg-spin"},
            {"name": "Ravichandran Ashwin",   "econ": 7.8, "death_econ": 9.5,  "wkts": 12, "form": 72, "type": "off-spin"},
            {"name": "Sandeep Sharma",        "econ": 8.2, "death_econ": 8.8,  "wkts": 10, "form": 65, "type": "fast-medium"},
            {"name": "Kuldeep Sen",           "econ": 9.0, "death_econ": 9.5,  "wkts": 8,  "form": 60, "type": "pace"},
        ],
        "squad": [
            {"name": "Riyan Parag",        "role": "allrounder", "form": 72},
            {"name": "Jason Holder",       "role": "allrounder", "form": 68},
            {"name": "Obed McCoy",         "role": "bowl",       "form": 62},
        ],
    },
}

VENUES = {
    "Wankhede, Mumbai":           {"avg": 185, "dew": True,  "pace": True,  "spin_assist": False},
    "Chinnaswamy, Bengaluru":     {"avg": 192, "dew": True,  "pace": False, "spin_assist": False},
    "Chepauk, Chennai":           {"avg": 162, "dew": False, "pace": False, "spin_assist": True},
    "Eden Gardens, Kolkata":      {"avg": 178, "dew": True,  "pace": True,  "spin_assist": False},
    "Arun Jaitley, Delhi":        {"avg": 175, "dew": False, "pace": True,  "spin_assist": False},
    "Sawai Mansingh, Jaipur":     {"avg": 170, "dew": False, "pace": False, "spin_assist": True},
    "Rajiv Gandhi, Hyderabad":    {"avg": 183, "dew": True,  "pace": True,  "spin_assist": False},
    "BRSABV Ekana, Lucknow":      {"avg": 171, "dew": True,  "pace": False, "spin_assist": True},
}
