# 🛡️ Sipahi — Fortress of Digital Finance

Sipahi is an autonomous multi-agent AI system that detects financial scams (SMS/WhatsApp) in
Roman Urdu, Urdu, and English — explaining verdicts in plain Urdu and feeding every report into
a live, crowdsourced fraud-intelligence network.

Built for the **Alibaba Cloud AI Hackathon 2026** (Bano Qabil × Alkhidmat Foundation Pakistan) —
Financial Inclusion track.

## ✨ Features

- **Multi-agent reasoning pipeline** — Parser → Pattern-Match → Risk-Reasoning → Network agents
- **Trust/Risk Score gauge** (0-100) with visual indicator
- **Risk category radar chart** — urgency, fake authority, money request, phishing links, emotional pressure
- **Red flag detection & chips**
- **OTP leak risk alert** — special high-priority warning
- **Plain-language Urdu explanations**
- **Live fraud dashboard** — trend charts, scam-type distribution, live scam network graph
- **Community Shield Score** — gamified impact per report
- **Shareable verdict card**
- **Bank/Fintech integration demo** — simulated webhook + compliance audit trail concept

## 🧱 Tech Stack

- Streamlit (UI)
- Groq (Llama 3.3 70B) for LLM-based scam reasoning
- Plotly + NetworkX for interactive visualizations
- Python-dotenv for local secret management

## 🚀 Running Locally

1. Clone the repo and enter the folder:
   ```bash
   git clone <your-repo-url>
   cd sipahi
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your own Groq API key:
   ```bash
   cp .env.example .env
   # then edit .env and paste your key
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🔐 Security Note

This repository contains **no secrets**. See `.env.example` for the required environment
variable. Never commit a real `.env` file or API key.

## 🏆 Hackathon Context

- **Focus Area:** Financial Inclusion
- **Team:** Umamah & Huzaifa
- **Problem:** SMS/WhatsApp financial scams (OTP phishing, fake investments, job scams, loan
  sharks, fake prizes) disproportionately harm low-digital-literacy users in Pakistan who read
  only Urdu/Roman Urdu.
- **Solution:** Sipahi — an agentic AI fraud-detection layer designed to plug into consumer apps
  today and bank/fintech SMS gateways tomorrow.
