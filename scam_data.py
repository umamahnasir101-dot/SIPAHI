from datetime import datetime, timedelta
import random

random.seed(7)

SCAM_PATTERNS = [
    "Aap ka JazzCash account block ho jayega, turant OTP bhejein",
    "Congratulations! Aap ne lucky draw mein 500000 jeeta hai",
    "Sirf 5000 invest karein, 1 hafte mein double profit guaranteed",
    "Job confirm hai, pehle 2000 processing fee bhejein",
    "Asaan loan, bina documents, sirf abhi apply karein",
    "Masjid tameer ke liye zakat bhejein is account mein",
]

base = datetime.now() - timedelta(days=13)
TREND_DATA = {
    "date": [(base + timedelta(days=i)).strftime("%b %d") for i in range(14)],
    "reports": [random.randint(40, 130) for _ in range(14)]
}
# make it trend upward toward "today" for dramatic effect
TREND_DATA["reports"] = sorted(TREND_DATA["reports"])[:10] + sorted(TREND_DATA["reports"][10:], reverse=False)

NETWORK_DATA = {
    "nodes": [
        {"id": "Campaign: OTP-Block", "group": "campaign"},
        {"id": "+92300xxxx11", "group": "number"},
        {"id": "+92311xxxx45", "group": "number"},
        {"id": "+92345xxxx09", "group": "number"},
        {"id": "Pattern: Fake Bank Alert", "group": "pattern"},
        {"id": "Campaign: Lucky-Draw", "group": "campaign"},
        {"id": "+92301xxxx78", "group": "number"},
        {"id": "+92333xxxx22", "group": "number"},
        {"id": "Pattern: Prize Fee Request", "group": "pattern"},
        {"id": "Campaign: Invest-Fast", "group": "campaign"},
        {"id": "+92321xxxx90", "group": "number"},
    ],
    "edges": [
        ("Campaign: OTP-Block", "+92300xxxx11"),
        ("Campaign: OTP-Block", "+92311xxxx45"),
        ("Campaign: OTP-Block", "+92345xxxx09"),
        ("Campaign: OTP-Block", "Pattern: Fake Bank Alert"),
        ("Campaign: Lucky-Draw", "+92301xxxx78"),
        ("Campaign: Lucky-Draw", "+92333xxxx22"),
        ("Campaign: Lucky-Draw", "Pattern: Prize Fee Request"),
        ("Campaign: Invest-Fast", "+92321xxxx90"),
        ("Campaign: Invest-Fast", "Pattern: Prize Fee Request"),
    ]
}
