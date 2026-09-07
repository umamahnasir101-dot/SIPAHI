import os
import json
import re
from groq import Groq

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Add it to your .env file.")
    return Groq(api_key=api_key)

SYSTEM_PROMPT = """You are Sipahi, an expert fraud-detection AI for Pakistan, specialized in \
detecting financial scams in Roman Urdu, Urdu, and English SMS/WhatsApp messages \
(OTP phishing, fake investment schemes, job-fee scams, loan-shark offers, fake prize/lottery \
scams, fake charity requests).

Analyze the given message and respond ONLY with valid JSON (no markdown, no preamble) in this \
exact structure:

{
  "is_scam": true or false,
  "risk_score": integer 0-100,
  "category": "otp_phishing" | "fake_investment" | "job_scam" | "loan_shark" | "fake_prize" | "fake_charity" | "safe" | "other",
  "flags": ["short red flag phrase", "..."],
  "otp_risk": true or false,
  "radar": [urgency_0_100, fake_authority_0_100, money_request_0_100, link_phishing_0_100, emotional_pressure_0_100],
  "explanation_urdu": "2-3 sentence plain-language explanation IN URDU SCRIPT of why this is or isn't a scam",
  "tip": "one short actionable safety tip in English",
  "pattern_match": "percentage-like short string, e.g. '87% match to known OTP scam pattern' or 'No strong match'"
}

Be decisive and realistic. If the message is clearly benign (e.g. a normal personal text), \
set is_scam to false and risk_score low. Always return valid JSON only."""

def analyze_message(message: str) -> dict:
    client = get_client()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0.3,
        max_tokens=600,
    )
    raw = completion.choices[0].message.content.strip()
    raw = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        data = json.loads(raw)
    except Exception:
        data = {
            "is_scam": True,
            "risk_score": 50,
            "category": "other",
            "flags": ["Could not fully parse — manual review suggested"],
            "otp_risk": False,
            "radar": [50, 50, 50, 50, 50],
            "explanation_urdu": "یہ پیغام مشکوک ہو سکتا ہے، احتیاط سے کام لیں۔",
            "tip": "Do not share OTPs or personal financial details.",
            "pattern_match": "N/A"
        }
    # safety defaults
    data.setdefault("flags", [])
    data.setdefault("radar", [50, 50, 50, 50, 50])
    data.setdefault("otp_risk", False)
    data.setdefault("pattern_match", "N/A")
    return data
