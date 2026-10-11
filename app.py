import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import json
import os
import re
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from logo_data import LOGO_HERO, LOGO_NAV

load_dotenv()

from groq_client import analyze_message
from scam_data import SCAM_PATTERNS, TREND_DATA, NETWORK_DATA

st.set_page_config(
    page_title="Sipahi — Fortress of Digital Finance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- GLOBAL THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #0f3d2e, #062018, #0e3a29, #04140e);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    color: #eef7f0;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

@keyframes floatUp {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-8px);}
    100% {transform: translateY(0px);}
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(12px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes pulseGlow {
    0% {box-shadow: 0 0 10px rgba(217,196,122,0.15);}
    50% {box-shadow: 0 0 25px rgba(217,196,122,0.4);}
    100% {box-shadow: 0 0 10px rgba(217,196,122,0.15);}
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    max-width: 1150px;
}

/* Hero */
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: 4px;
    color: #f2ecd8;
    text-align: center;
    margin-bottom: 0;
    text-shadow: 0 0 25px rgba(120,255,180,0.25);
    animation: fadeIn 1s ease;
}
.hero-sub {
    text-align: center;
    color: #a9d8bf;
    letter-spacing: 3px;
    font-size: 1.1rem;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
    animation: fadeIn 1.3s ease;
}
.hero-line {
    height: 2px;
    width: 220px;
    margin: 0 auto 2.2rem auto;
    background: linear-gradient(90deg, transparent, #c9a24a, transparent);
}

.logo-glow img {
    animation: floatUp 5s ease-in-out infinite;
    filter: drop-shadow(0 0 30px rgba(120,255,180,0.35));
}

.back-btn-row {
    margin-bottom: 0.5rem;
}

/* Card */
.sipahi-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
    border: 1px solid rgba(120,255,180,0.15);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    animation: fadeIn 0.6s ease;
    transition: all 0.3s ease;
}
.sipahi-card:hover {
    border-color: rgba(217,196,122,0.5);
    transform: translateY(-3px);
}

.metric-box {
    text-align:center;
    padding: 1rem;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(201,162,74,0.25);
    animation: floatUp 4s ease-in-out infinite, fadeIn 0.6s ease;
    transition: all 0.3s ease;
}
.metric-box:hover {
    animation: pulseGlow 1.5s ease infinite;
    border-color: #d9c47a;
}
.metric-num {
    font-size: 2.1rem;
    font-weight: 800;
    color: #d9c47a;
}
.metric-label {
    color: #a9d8bf;
    font-size: 0.85rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Nav buttons */
div.stButton > button {
    background: linear-gradient(135deg, #1c5c41, #0e3a29);
    color: #f2ecd8 !important;
    border: 1px solid rgba(201,162,74,0.4);
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.2s ease;
    width: 100%;
}
div.stButton > button:hover {
    border-color: #d9c47a;
    box-shadow: 0 0 18px rgba(201,162,74,0.4);
    transform: translateY(-2px);
    color: #fff !important;
}

.flag-chip {
    display:inline-block;
    background: rgba(220,80,80,0.15);
    border: 1px solid rgba(220,80,80,0.5);
    color: #ffb4b4;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.85rem;
}
.safe-chip {
    display:inline-block;
    background: rgba(90,200,140,0.15);
    border: 1px solid rgba(90,200,140,0.5);
    color: #bdf2d0;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.85rem;
}

.verdict-scam {
    font-size: 1.8rem;
    font-weight: 800;
    color: #ff6b6b;
    text-align:center;
}
.verdict-safe {
    font-size: 1.8rem;
    font-weight: 800;
    color: #6bffb0;
    text-align:center;
}

.section-title {
    color: #d9c47a;
    font-weight: 700;
    font-size: 1.3rem;
    margin-bottom: 0.6rem;
    border-left: 4px solid #d9c47a;
    padding-left: 10px;
}

a { color: #d9c47a !important; }

/* ---- Branding ---- */
.brand-bar {display:flex; align-items:center; gap:12px; padding:2px 0;}
.brand-bar img {height:62px; filter: drop-shadow(0 0 12px rgba(120,255,180,0.35));}
.brand-name {font-size:1.7rem; font-weight:800; letter-spacing:4px; color:#f2ecd8; line-height:1;}
.brand-tag {font-size:0.62rem; letter-spacing:2.5px; color:#a9d8bf; margin-top:5px;}

.hero-wrap {text-align:center; padding: 0.5rem 0 0.5rem 0; position:relative;}
.hero-logo {width:230px; max-width:60%; animation: floatUp 5s ease-in-out infinite;
            filter: drop-shadow(0 0 35px rgba(120,255,180,0.45));}
.hero-glow {position:absolute; left:50%; top:60px; width:320px; height:320px; margin-left:-160px;
            background: radial-gradient(circle, rgba(120,255,180,0.18), transparent 65%);
            animation: pulseGlow 4s ease-in-out infinite; border-radius:50%; z-index:0;}
.hero-wrap img, .hero-wrap div {position:relative; z-index:1;}
.hero-name {font-size:4.2rem; font-weight:800; letter-spacing:10px; margin-top:0.4rem;
            background: linear-gradient(90deg, #f2ecd8, #d9c47a, #f2ecd8);
            background-size: 200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            animation: shimmer 5s linear infinite;}
.hero-tagline {color:#a9d8bf; letter-spacing:5px; font-size:1rem; margin-top:-0.2rem;}
.hero-pill {display:inline-block; margin-top:1.1rem; padding:6px 18px; border-radius:30px;
            border:1px solid rgba(217,196,122,0.5); background:rgba(14,58,41,0.7);
            color:#d9c47a; font-size:0.8rem; letter-spacing:1.5px; font-weight:600;}
@keyframes shimmer {to {background-position: 200% center;}}

.floaty-dots {position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden;}
.floaty-dots span {position:absolute; border-radius:50%; background:rgba(120,255,180,0.10);
                    animation: drift 14s ease-in-out infinite;}
@keyframes drift {0%,100% {transform:translateY(0) scale(1);} 50% {transform:translateY(-40px) scale(1.15);}}

.site-footer {text-align:center; color:#7fb597; font-size:0.78rem; letter-spacing:1.5px;
              margin-top:3rem; padding-top:1rem; border-top:1px solid rgba(217,196,122,0.2);}
.feat-card {text-align:center; font-weight:600;}
.feat-card .ico {font-size:1.8rem; display:block; margin-bottom:6px;}
.feat-card small {display:block; color:#a9d8bf; font-weight:400; margin-top:4px;}
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reports_count" not in st.session_state:
    st.session_state.reports_count = 1847
if "rupees_saved" not in st.session_state:
    st.session_state.rupees_saved = 4_285_000
if "history" not in st.session_state:
    st.session_state.history = []

def goto(page):
    st.session_state.page = page

# ---------------- TOP NAV ----------------
def back_button():
    if st.session_state.page != "home":
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("← Back to Home", key="back_btn"):
                goto("home")
        st.markdown("<br>", unsafe_allow_html=True)

def top_nav():
    brand_c, nav_c = st.columns([2, 7])
    with brand_c:
        st.markdown(f"""<div class='brand-bar'>
            <img src='data:image/png;base64,{LOGO_NAV}'/>
            <div><div class='brand-name'>SIPAHI</div>
            <div class='brand-tag'>FORTRESS OF DIGITAL FINANCE</div></div></div>""",
            unsafe_allow_html=True)
    with nav_c:
        cols = st.columns(5)
        labels = [("🏠 Home", "home"), ("🔍 Scam Checker", "checker"),
                  ("📊 Dashboard", "dashboard"), ("🏦 For Banks", "api"),
                  ("ℹ️ How It Works", "about")]
        for c, (label, key) in zip(cols, labels):
            with c:
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    goto(key)
    st.markdown("<div class='hero-line' style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)

# ================= HOME =================
def page_home():
    st.markdown(f"""
    <div class='hero-wrap'>
        <div class='hero-glow'></div>
        <img class='hero-logo' src='data:image/png;base64,{LOGO_HERO}'/>
        <div class='hero-name'>SIPAHI</div>
        <div class='hero-tagline'>FORTRESS OF DIGITAL FINANCE</div>
        <div class='hero-pill'>ALIBABA CLOUD AI HACKATHON 2026 &nbsp;·&nbsp; FINANCIAL INCLUSION</div>
    </div>
    <div class='hero-line' style='margin-top:1.5rem;'></div>
    <div style='text-align:center; max-width:720px; margin:0 auto 2rem auto; color:#dfeee0; font-size:1.05rem; line-height:1.7;'>
    Sipahi is an autonomous multi-agent AI system that reads suspicious SMS &amp; WhatsApp messages
    in <b>Roman Urdu / Urdu</b>, tells you instantly whether it's a scam and why, and feeds every
    report into a live, crowdsourced fraud-intelligence network — protecting the next person automatically.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{st.session_state.reports_count:,}", "Scams Reported"),
        (f"Rs {st.session_state.rupees_saved/1_000_000:.2f}M", "Est. Losses Prevented"),
        ("4", "AI Agents Working"),
        ("24/7", "Protection")
    ]
    for c, (num, label) in zip([c1, c2, c3, c4], stats):
        with c:
            st.markdown(f"""<div class='metric-box'><div class='metric-num'>{num}</div>
            <div class='metric-label'>{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔍  Check a Message Now", use_container_width=True):
            goto("checker")
    with c2:
        if st.button("📊  View Live Fraud Dashboard", use_container_width=True):
            goto("dashboard")
    with c3:
        if st.button("🏦  Bank Integration Demo", use_container_width=True):
            goto("api")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>What Sipahi Detects</div>", unsafe_allow_html=True)
    cats = [("💳", "OTP / Banking Phishing", "Fake bank & wallet alerts"),
            ("📈", "Fake Investment Schemes", "\"Guaranteed\" returns, Ponzi pitches"),
            ("💼", "Job Offer Scams", "Pay-to-get-hired traps"),
            ("🏦", "Loan Shark Offers", "Predatory instant-loan SMS"),
            ("🎁", "Fake Prize / Lottery", "CNIC & fee-harvesting draws"),
            ("🕌", "Fake Charity Requests", "Zakat & donation impersonation")]
    cols = st.columns(3)
    for i, (ico, name, sub) in enumerate(cats):
        with cols[i % 3]:
            st.markdown(f"<div class='sipahi-card feat-card'><span class='ico'>{ico}</span>{name}<small>{sub}</small></div>", unsafe_allow_html=True)

    st.markdown("<div class='site-footer'>🛡️ SIPAHI · Fortress of Digital Finance · Built by Umamah &amp; Huzaifa</div>", unsafe_allow_html=True)

# ================= SCAM CHECKER =================
def page_checker():
    st.markdown("<div class='section-title'>🔍 Scam Message Checker</div>", unsafe_allow_html=True)
    st.write("Paste any suspicious SMS or WhatsApp message (Roman Urdu, Urdu, or English) below.")

    msg = st.text_area("Message to analyze", height=120,
                        placeholder="e.g. Aap ka JazzCash account block ho jayega. Turant apna OTP is number par bhejein...")

    example_cols = st.columns(3)
    examples = [
        "Congratulations! Aap ne 500,000 rupay ka lucky draw jeeta hai. Claim karne ke liye apna CNIC aur account number bhejein.",
        "Sirf 5000 invest karein aur 1 hafte mein 50000 kamayein! Guaranteed profit, limited seats.",
        "Ammi jaisa theek hain? Kal party hai ghar per, aa jana."
    ]
    ex_labels = ["🎁 Try: Prize Scam", "📈 Try: Investment Scam", "✅ Try: Safe Message"]
    for c, ex, lab in zip(example_cols, examples, ex_labels):
        with c:
            if st.button(lab, use_container_width=True):
                msg = ex
                st.session_state["prefill"] = ex

    if "prefill" in st.session_state and not msg:
        msg = st.session_state["prefill"]

    if st.button("🛡️ Analyze with Sipahi Agents", use_container_width=True) and msg.strip():
        with st.spinner("Agents at work: Parser → Pattern-Match → Risk-Reasoning → Network..."):
            result = analyze_message(msg)
        st.session_state.history.append({"msg": msg, "result": result, "time": datetime.now()})
        st.session_state.reports_count += 1
        if result["is_scam"]:
            st.session_state.rupees_saved += random.randint(15000, 120000)
        render_result(result, msg)

    if st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
        st.markdown("<b>🕓 Your Scan History (this session)</b>", unsafe_allow_html=True)
        rows = []
        for h in reversed(st.session_state.history):
            r = h["result"]
            rows.append({
                "Time": h["time"].strftime("%I:%M %p"),
                "Message": h["msg"][:50] + ("..." if len(h["msg"]) > 50 else ""),
                "Category": r.get("category", "other").replace("_", " ").title(),
                "Risk Score": r["risk_score"],
                "Verdict": "⚠️ Scam" if r["is_scam"] else "✅ Safe"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_result(result, msg):
    st.markdown("<br>", unsafe_allow_html=True)

    # Agent trace
    st.markdown("<div class='section-title'>🤖 Agent Reasoning Trace</div>", unsafe_allow_html=True)
    steps = [
        ("Parser Agent", "Cleaned & normalized Roman Urdu/Urdu text, detected code-switching."),
        ("Pattern-Match Agent", f"Compared against known scam database — similarity: {result.get('pattern_match','N/A')}"),
        ("Risk-Reasoning Agent", "Evaluated urgency, authority-impersonation & payment-request signals."),
        ("Network Agent", "Logged pattern to crowdsourced fraud-intelligence graph." if result["is_scam"] else "No new pattern needed — message looks safe.")
    ]
    cols = st.columns(4)
    for c, (name, desc) in zip(cols, steps):
        with c:
            st.markdown(f"<div class='sipahi-card' style='min-height:120px;'><b>⚙️ {name}</b><br><small>{desc}</small></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1, 1])

    with left:
        verdict_class = "verdict-scam" if result["is_scam"] else "verdict-safe"
        verdict_text = "⚠️ SCAM DETECTED" if result["is_scam"] else "✅ LOOKS SAFE"
        st.markdown(f"<div class='sipahi-card'><div class='{verdict_class}'>{verdict_text}</div>", unsafe_allow_html=True)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["risk_score"],
            number={'suffix': "/100", 'font': {'color': '#f2ecd8'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#a9d8bf'},
                'bar': {'color': '#d9c47a'},
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(90,200,140,0.35)'},
                    {'range': [30, 65], 'color': 'rgba(220,180,80,0.35)'},
                    {'range': [65, 100], 'color': 'rgba(220,80,80,0.35)'}
                ],
            },
            title={'text': "Risk Score", 'font': {'color': '#d9c47a'}}
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#eef7f0"}, height=280, margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if result.get("otp_risk"):
            st.markdown("<div class='sipahi-card' style='border-color:#ff6b6b;'>🚨 <b>OTP LEAK RISK</b> — this message is trying to extract a one-time password or account credential. Never share OTPs with anyone.</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
        st.markdown("<b>🚩 Red Flags Detected</b><br><br>", unsafe_allow_html=True)
        if result["flags"]:
            chips = "".join([f"<span class='flag-chip'>{f}</span>" for f in result["flags"]])
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.markdown("<span class='safe-chip'>No red flags detected</span>", unsafe_allow_html=True)

        st.markdown("<br><br><b>📊 Risk Category Breakdown</b>", unsafe_allow_html=True)
        radar = go.Figure()
        cats = ["Urgency", "Fake Authority", "Money Request", "Link/Phishing", "Emotional Pressure"]
        radar.add_trace(go.Scatterpolar(r=result["radar"], theta=cats, fill='toself',
                                          line_color='#d9c47a', fillcolor='rgba(217,196,122,0.3)'))
        radar.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
                                        radialaxis=dict(visible=True, range=[0,100], color="#a9d8bf")),
                             showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                             font={'color': "#eef7f0"}, height=280, margin=dict(t=20,b=20,l=40,r=40))
        st.plotly_chart(radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
    st.markdown("<b>🗣️ Explanation (Urdu)</b><br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:1.1rem; line-height:1.8;'>{result['explanation_urdu']}</div>", unsafe_allow_html=True)
    st.markdown("<br><b>💡 Safety Tip</b><br>" + result.get("tip", ""), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class='sipahi-card' style='text-align:center;'>
        🛡️ <b>Community Shield Score</b><br>
        <span class='metric-num'>+{random.randint(12,48)}</span><br>
        <span class='metric-label'>People protected by this report</span></div>""", unsafe_allow_html=True)
    with c2:
        if st.button("📤 Generate Shareable Verdict Card", use_container_width=True):
            st.success("Verdict card generated — share it to warn friends & family!")
            st.markdown(f"""
            <div class='sipahi-card' style='border:2px solid #d9c47a; text-align:center;'>
            🛡️ SIPAHI VERDICT<br><b style='font-size:1.4rem;'>{verdict_text}</b><br>
            Risk Score: {result['risk_score']}/100<br>
            <small>Verified by Sipahi AI — Fortress of Digital Finance</small>
            </div>""", unsafe_allow_html=True)

# ================= DASHBOARD =================
def page_dashboard():
    st.markdown("<div class='section-title'>📊 Live Fraud Intelligence Dashboard</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (f"{st.session_state.reports_count:,}", "Total Reports"),
        (f"Rs {st.session_state.rupees_saved/1_000_000:.2f}M", "Losses Prevented"),
        ("Karachi", "Top Hotspot"),
        ("OTP Phishing", "Top Scam Type")
    ]
    for c, (num, label) in zip([c1, c2, c3, c4], stats):
        with c:
            st.markdown(f"<div class='metric-box'><div class='metric-num'>{num}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
        st.markdown("<b>📈 Scam Reports Trend (Last 14 Days)</b>", unsafe_allow_html=True)
        df = pd.DataFrame(TREND_DATA)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["reports"], mode='lines+markers',
                                  line=dict(color='#d9c47a', width=3), fill='tozeroy',
                                  fillcolor='rgba(217,196,122,0.15)'))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font={'color': "#eef7f0"}, height=300, margin=dict(t=10,b=10,l=10,r=10),
                           xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                           yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
        st.markdown("<b>🍰 Scam Types Distribution</b>", unsafe_allow_html=True)
        types = ["OTP Phishing", "Fake Investment", "Job Scam", "Loan Shark", "Fake Prize", "Charity Scam"]
        vals = [32, 22, 18, 12, 10, 6]
        fig2 = go.Figure(data=[go.Pie(labels=types, values=vals, hole=0.5,
                                       marker=dict(colors=['#d9c47a','#8fd6ac','#1c5c41','#c9a24a','#6bffb0','#3d7a5c']))])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#eef7f0"}, height=300,
                            margin=dict(t=10,b=10,l=10,r=10), showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
    st.markdown("<b>🕸️ Live Scam Network Graph</b><br><small>Nodes = reported numbers/patterns · Edges = shared scam campaign</small>", unsafe_allow_html=True)
    G = nx.Graph()
    for node in NETWORK_DATA["nodes"]:
        G.add_node(node["id"], group=node["group"])
    for edge in NETWORK_DATA["edges"]:
        G.add_edge(edge[0], edge[1])
    pos = nx.spring_layout(G, seed=42, k=0.6)

    edge_x, edge_y = [], []
    for e in G.edges():
        x0, y0 = pos[e[0]]; x1, y1 = pos[e[1]]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='rgba(217,196,122,0.4)'), hoverinfo='none', mode='lines')

    node_x, node_y, node_color, node_text = [], [], [], []
    color_map = {"campaign": "#ff6b6b", "number": "#d9c47a", "pattern": "#6bffb0"}
    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x); node_y.append(y)
        node_color.append(color_map.get(G.nodes[n]["group"], "#8fd6ac"))
        node_text.append(n)
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
                             textfont=dict(color="#eef7f0", size=10),
                             marker=dict(size=22, color=node_color, line=dict(width=2, color='#0e3a29')))

    fig3 = go.Figure(data=[edge_trace, node_trace])
    fig3.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=420, margin=dict(t=10,b=10,l=10,r=10),
                        xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
    st.markdown("<b>📋 Recent Community Reports</b>", unsafe_allow_html=True)
    sample_reports = [
        {"Time": "2 min ago", "Category": "OTP Phishing", "Risk Score": 94, "City": "Lahore", "Status": "🔴 Confirmed Scam"},
        {"Time": "18 min ago", "Category": "Fake Investment", "Risk Score": 88, "City": "Karachi", "Status": "🔴 Confirmed Scam"},
        {"Time": "41 min ago", "Category": "Job Scam", "Risk Score": 76, "City": "Islamabad", "Status": "🟠 Likely Scam"},
        {"Time": "1 hr ago", "Category": "Fake Prize", "Risk Score": 91, "City": "Faisalabad", "Status": "🔴 Confirmed Scam"},
        {"Time": "2 hr ago", "Category": "Loan Shark", "Risk Score": 68, "City": "Rawalpindi", "Status": "🟠 Likely Scam"},
        {"Time": "3 hr ago", "Category": "Safe Message", "Risk Score": 8, "City": "Multan", "Status": "🟢 Safe"},
    ]
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            r = h["result"]
            sample_reports.insert(0, {
                "Time": h["time"].strftime("%I:%M %p"),
                "Category": r.get("category", "other").replace("_", " ").title(),
                "Risk Score": r["risk_score"],
                "City": "Your Report",
                "Status": "🔴 Confirmed Scam" if r["is_scam"] else "🟢 Safe"
            })
    df_reports = pd.DataFrame(sample_reports)
    st.dataframe(df_reports, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= API / BANK PAGE =================
def page_api():
    st.markdown("<div class='section-title'>🏦 Sipahi for Banks & Fintechs</div>", unsafe_allow_html=True)
    st.write("Sipahi is designed to plug directly into an SMS gateway, banking app, or fintech platform — flagging fraud before it reaches the customer.")

    st.markdown("<div class='sipahi-card'>", unsafe_allow_html=True)
    st.markdown("<b>🔌 Simulated Webhook Integration</b>", unsafe_allow_html=True)
    st.code("""
POST https://api.sipahi.ai/v1/analyze
Headers: { "Authorization": "Bearer <BANK_API_KEY>" }
Body: {
  "message": "Aap ka account block ho jayega, OTP bhejein...",
  "channel": "sms",
  "customer_id": "cust_88213"
}

Response: {
  "is_scam": true,
  "risk_score": 92,
  "category": "otp_phishing",
  "action": "block_and_alert_customer",
  "compliance_log_id": "sip_20260904_00931"
}
""", language="json")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='sipahi-card'>
        <b>📋 Compliance-Ready Audit Trail</b><br><br>
        Every classification is logged with timestamp, reasoning, and confidence — exportable
        for fraud teams and regulators.<br><br>
        <span class='safe-chip'>Explainable AI</span>
        <span class='safe-chip'>Timestamped</span>
        <span class='safe-chip'>Exportable</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='sipahi-card'>
        <b>💰 Estimated ROI for a Mid-Size Bank</b><br><br>
        Based on current fraud-reporting trends, Sipahi-style pre-screening could prevent an
        estimated <b>Rs 15-40M</b> in annual customer fraud losses for a mid-size digital bank,
        while reducing fraud-team manual review load.
        </div>""", unsafe_allow_html=True)

# ================= ABOUT =================
def page_about():
    st.markdown("<div class='section-title'>ℹ️ How Sipahi Works</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sipahi-card'>
    <b>The Problem:</b> SMS & WhatsApp financial scams (OTP phishing, fake investments, job scams,
    loan sharks, fake prizes) are surging across Pakistan, disproportionately hurting people with
    lower digital literacy who read only Urdu or Roman Urdu.
    </div>
    <div class='sipahi-card'>
    <b>The Solution:</b> A multi-agent AI pipeline — Parser, Pattern-Match, Risk-Reasoning, and
    Network agents — analyzes any forwarded message in seconds, explains the verdict in plain Urdu,
    and adds new scam patterns to a shared, crowdsourced fraud-intelligence graph so every report
    protects the next potential victim.
    </div>
    <div class='sipahi-card'>
    <b>Tech Stack:</b> LLM reasoning (Groq/Llama), agentic pipeline orchestration, NLP for Roman
    Urdu/Urdu normalization, network-graph fraud intelligence, Streamlit interface, Power BI-ready
    analytics layer.
    </div>
    <div class='sipahi-card'>
    <b>Why It Matters:</b> This isn't just a consumer tool — it's designed to plug directly into
    banks and fintech SMS gateways as fraud-prevention infrastructure, opening a real path to
    commercialization.
    </div>
    """, unsafe_allow_html=True)

# ================= ROUTER =================
st.markdown("""<div class='floaty-dots'>
<span style='width:180px;height:180px;left:8%;top:25%;animation-delay:0s;'></span>
<span style='width:120px;height:120px;left:82%;top:15%;animation-delay:2s;'></span>
<span style='width:220px;height:220px;left:70%;top:62%;animation-delay:4s;'></span>
<span style='width:90px;height:90px;left:20%;top:72%;animation-delay:6s;'></span>
</div>""", unsafe_allow_html=True)
top_nav()
back_button()
page = st.session_state.page
if page == "home":
    page_home()
elif page == "checker":
    page_checker()
elif page == "dashboard":
    page_dashboard()
elif page == "api":
    page_api()
elif page == "about":
    page_about()

if page != "home":
    st.markdown("<div class='site-footer'>🛡️ SIPAHI · Fortress of Digital Finance · Built by Umamah &amp; Huzaifa</div>", unsafe_allow_html=True)
