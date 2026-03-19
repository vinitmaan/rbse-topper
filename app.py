import streamlit as st
import urllib.parse
import time
import base64
from groq import Groq

# ==========================================
# 1. PAGE CONFIG & SECRETS VALIDATION
# ==========================================
st.set_page_config(
    page_title="HEXALOY AI",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 System Error: GROQ_API_KEY is missing in Streamlit Secrets!")
    st.stop()

# ==========================================
# 2. FULL CSS — ANIMATIONS + DARK/LIGHT MODE
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* ══ CSS VARIABLES — LIGHT MODE ══ */
:root {
    --bg-primary:        #F0F4FF;
    --bg-surface:        #FFFFFF;
    --bg-surface-alt:    #E8EEF9;
    --bg-sidebar:        #FFFFFF;
    --border:            #D4DCF0;
    --text-primary:      #0B0F1E;
    --text-secondary:    #4A5470;
    --text-muted:        #8891AB;
    --accent:            #1B4FD8;
    --accent2:           #5B8BFF;
    --accent-subtle:     #EBF0FD;
    --msg-user-bg:       #EBF0FD;
    --msg-user-border:   #C0CFF7;
    --msg-ai-bg:         #FFFFFF;
    --msg-ai-border:     #D4DCF0;
    --input-bg:          #FFFFFF;
    --glow:              rgba(27, 79, 216, 0.18);
    --orb1:              rgba(27, 79, 216, 0.08);
    --orb2:              rgba(91, 139, 255, 0.06);
    --particle:          rgba(27, 79, 216, 0.3);
    --shadow-sm:         0 2px 8px rgba(27,79,216,0.07);
    --shadow-md:         0 6px 24px rgba(27,79,216,0.10);
    --shadow-glow:       0 0 30px rgba(27,79,216,0.15);
}

/* ══ CSS VARIABLES — DARK MODE ══ */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary:        #080C18;
        --bg-surface:        #0F1628;
        --bg-surface-alt:    #151D35;
        --bg-sidebar:        #0C1020;
        --border:            #1E2A45;
        --text-primary:      #E2E8F8;
        --text-secondary:    #7A86A8;
        --text-muted:        #3E4A6A;
        --accent:            #4A7CF7;
        --accent2:           #7BA7FF;
        --accent-subtle:     #111D3A;
        --msg-user-bg:       #111D3A;
        --msg-user-border:   #1E3060;
        --msg-ai-bg:         #0F1628;
        --msg-ai-border:     #1E2A45;
        --input-bg:          #0F1628;
        --glow:              rgba(74, 124, 247, 0.25);
        --orb1:              rgba(74, 124, 247, 0.10);
        --orb2:              rgba(123, 167, 255, 0.06);
        --particle:          rgba(74, 124, 247, 0.55);
        --shadow-sm:         0 2px 8px rgba(0,0,0,0.4);
        --shadow-md:         0 6px 24px rgba(0,0,0,0.5);
        --shadow-glow:       0 0 40px rgba(74,124,247,0.20);
    }
}

/* ══ KEYFRAME ANIMATIONS ══ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.92); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes orbFloat {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(30px,-20px) scale(1.05); }
    66%      { transform: translate(-20px,15px) scale(0.97); }
}
@keyframes orbFloat2 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%      { transform: translate(-25px,20px) scale(1.04); }
    70%      { transform: translate(20px,-15px) scale(0.96); }
}
@keyframes pulseRing {
    0%   { transform:scale(0.95); box-shadow:0 0 0 0 var(--glow); }
    70%  { transform:scale(1);    box-shadow:0 0 0 10px rgba(74,124,247,0); }
    100% { transform:scale(0.95); box-shadow:0 0 0 0 rgba(74,124,247,0); }
}
@keyframes typingDot {
    0%,60%,100% { transform:translateY(0); opacity:0.4; }
    30%          { transform:translateY(-7px); opacity:1; }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes messageSlideIn {
    from { opacity:0; transform:translateY(14px) scale(0.98); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes sidebarItemIn {
    from { opacity:0; transform:translateX(-12px); }
    to   { opacity:1; transform:translateX(0); }
}
@keyframes logoGlow {
    0%,100% { filter: drop-shadow(0 0 0px transparent); }
    50%      { filter: drop-shadow(0 0 12px var(--glow)); }
}
@keyframes floatBadge {
    0%,100% { transform:translateY(0px); }
    50%      { transform:translateY(-4px); }
}
@keyframes particleDrift {
    0%   { transform:translateY(100vh) scale(0); opacity:0; }
    10%  { opacity:1; }
    90%  { opacity:0.5; }
    100% { transform:translateY(-10vh) translateX(30px) scale(1); opacity:0; }
}
@keyframes borderPulse {
    0%,100% { border-color:var(--border); }
    50%      { border-color:var(--accent); box-shadow:0 0 14px var(--glow); }
}
@keyframes spin {
    to { transform:rotate(360deg); }
}

/* ══ GLOBAL ══ */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    transition: background-color 0.4s ease, color 0.4s ease;
}
#MainMenu{visibility:hidden;} footer{visibility:hidden;} .stDeployButton{display:none;}

/* ══ BACKGROUND ORBS ══ */
.main::before {
    content:''; position:fixed; top:-10%; right:-5%;
    width:520px; height:520px;
    background:radial-gradient(circle, var(--orb1) 0%, transparent 70%);
    border-radius:50%;
    animation:orbFloat 12s ease-in-out infinite;
    pointer-events:none; z-index:0;
}
.main::after {
    content:''; position:fixed; bottom:5%; left:-8%;
    width:440px; height:440px;
    background:radial-gradient(circle, var(--orb2) 0%, transparent 70%);
    border-radius:50%;
    animation:orbFloat2 15s ease-in-out infinite;
    pointer-events:none; z-index:0;
}

/* ══ MAIN CONTAINER ══ */
.main .block-container {
    padding-top:2rem !important;
    padding-bottom:5rem !important;
    max-width:860px;
    position:relative; z-index:1;
    animation:fadeInUp 0.6s cubic-bezier(0.22,1,0.36,1) both;
}

/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    animation: fadeInLeft 0.5s ease both;
    position:relative;
    overflow:hidden;
}
section[data-testid="stSidebar"]::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg, var(--accent), var(--accent2), var(--accent));
    background-size:200% auto;
    animation:gradientShift 3s linear infinite;
}
section[data-testid="stSidebar"] > div { padding:1.6rem 1rem !important; }

/* ══ BRAND NAME ══ */
.brand-name {
    font-family:'Syne', sans-serif !important;
    font-size:1.85rem !important;
    font-weight:800 !important;
    color: var(--text-primary) !important;
    letter-spacing:2.5px;
    animation:logoGlow 4s ease-in-out infinite;
    transition:letter-spacing 0.4s ease;
    cursor:default;
}
.brand-name:hover { letter-spacing:4px; }
.brand-logo-img {
    border-radius:10px;
    transition:transform 0.4s cubic-bezier(0.34,1.56,0.64,1);
    animation:floatBadge 3s ease-in-out infinite;
}
.brand-logo-img:hover { transform:rotate(15deg) scale(1.2) !important; }

/* ══ SIDEBAR BUTTONS ══ */
.stButton>button {
    width:100%; text-align:left;
    background-color:transparent; border:1px solid transparent;
    padding:10px 14px; border-radius:10px;
    font-family:'DM Sans', sans-serif; font-weight:500; font-size:0.875rem;
    color:var(--text-secondary) !important;
    transition:all 0.22s cubic-bezier(0.22,1,0.36,1);
    cursor:pointer; position:relative; overflow:hidden;
    animation:sidebarItemIn 0.4s ease both;
}
.stButton>button::after {
    content:''; position:absolute; left:-100%; top:0;
    width:100%; height:100%;
    background:linear-gradient(90deg, transparent, rgba(74,124,247,0.1), transparent);
    transition:left 0.5s ease;
}
.stButton>button:hover::after { left:100%; }
.stButton>button:hover {
    background-color:var(--bg-surface-alt) !important;
    color:var(--text-primary) !important;
    border-color:var(--border) !important;
    transform:translateX(5px);
    box-shadow:var(--shadow-sm);
}

/* ══ NEW SESSION BUTTON ══ */
.new-chat-btn>div>button {
    background:linear-gradient(135deg, var(--accent), var(--accent2), #6FA0FF) !important;
    background-size:200% 200% !important;
    animation:gradientShift 3s ease infinite !important;
    color:#FFFFFF !important;
    font-family:'Syne', sans-serif !important; font-weight:700 !important;
    font-size:0.9rem !important; letter-spacing:0.8px;
    text-align:center !important; justify-content:center;
    border-radius:12px !important; border:none !important;
    padding:12px 20px !important;
    box-shadow:0 4px 20px var(--glow) !important;
    margin-bottom:1.5rem;
    transition:all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
}
.new-chat-btn>div>button:hover {
    transform:translateY(-3px) scale(1.02) !important;
    box-shadow:0 10px 32px var(--glow), 0 0 0 4px rgba(74,124,247,0.15) !important;
}
.new-chat-btn>div>button:active { transform:translateY(-1px) scale(0.99) !important; }

/* ══ HISTORY LABEL ══ */
.history-label {
    font-family:'Syne', sans-serif; font-size:0.65rem; font-weight:700;
    letter-spacing:2px; text-transform:uppercase; color:var(--text-muted);
    margin:0 0 8px 4px; display:flex; align-items:center; gap:8px;
}
.history-label::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg, var(--border), transparent);
}

/* ══ SIGNATURE BOX ══ */
.signature-box {
    margin-top:28px; padding:14px 18px; border-radius:12px;
    background:var(--bg-surface-alt); border:1px solid var(--border);
    text-align:center; position:relative; overflow:hidden;
    transition:all 0.3s ease;
    animation:fadeInUp 0.5s ease 0.4s both;
}
.signature-box::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1.5px;
    background:linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
    background-size:200% auto;
    animation:gradientShift 3s linear infinite;
}
.signature-box:hover {
    box-shadow:var(--shadow-glow); transform:translateY(-2px);
    border-color:var(--accent);
    animation:borderPulse 2s ease infinite;
}
.sig-label  { margin:0; font-size:0.62rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:2px; }
.sig-name   { margin:5px 0 0; font-size:1.05rem; font-weight:800; font-family:'Syne',sans-serif; letter-spacing:1px;
               background:linear-gradient(135deg, var(--text-primary), var(--accent2));
               -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.sig-version{ margin:3px 0 0; font-size:0.62rem; color:var(--accent); letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }

/* ══ HERO ══ */
.hero-wrap {
    text-align:center; margin-bottom:2rem;
    animation:scaleIn 0.7s cubic-bezier(0.22,1,0.36,1) both;
    position:relative;
}
.hero-eyebrow {
    font-family:'Syne',sans-serif; font-size:0.65rem; font-weight:700;
    letter-spacing:4px; text-transform:uppercase; color:var(--accent);
    margin-bottom:10px; animation:fadeInDown 0.5s ease 0.1s both;
    display:flex; align-items:center; justify-content:center; gap:10px;
}
.hero-eyebrow::before,.hero-eyebrow::after { content:''; width:30px; height:1px; }
.hero-eyebrow::before { background:linear-gradient(90deg, transparent, var(--accent)); }
.hero-eyebrow::after  { background:linear-gradient(90deg, var(--accent), transparent); }
.hero-title {
    font-family:'Syne',sans-serif; font-size:clamp(2.2rem,5vw,3.2rem);
    font-weight:800; color:var(--text-primary); letter-spacing:-1px; line-height:1.05; margin:0;
    animation:fadeInUp 0.6s ease 0.15s both;
}
.hero-title .accent-word {
    background:linear-gradient(135deg, var(--accent), var(--accent2), #A8CAFF, var(--accent));
    background-size:300% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:shimmer 4s linear infinite;
}
.hero-subtitle {
    color:var(--text-secondary); font-size:0.97rem; font-weight:400;
    margin:12px 0 0; letter-spacing:0.3px;
    animation:fadeInUp 0.6s ease 0.25s both;
}
.status-badge {
    display:inline-flex; align-items:center; gap:6px;
    font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:500;
    color:var(--text-muted); padding:4px 12px;
    background:var(--bg-surface-alt); border:1px solid var(--border);
    border-radius:20px; margin:12px auto 0;
    animation:fadeInDown 0.5s ease 0.2s both;
    transition:all 0.3s ease;
}
.status-badge:hover { border-color:var(--accent); color:var(--text-secondary); box-shadow:var(--shadow-glow); }
.status-dot {
    width:7px; height:7px; background:#22C55E; border-radius:50%;
    animation:pulseRing 2s cubic-bezier(0.455,0.03,0.515,0.955) infinite;
}
.hero-dots { display:flex; align-items:center; justify-content:center; gap:6px; margin-top:16px; animation:fadeInUp 0.5s ease 0.35s both; }
.hero-dot  { width:6px; height:6px; border-radius:50%; background:var(--accent); opacity:0.3; animation:typingDot 1.8s ease-in-out infinite; }
.hero-dot:nth-child(2) { animation-delay:0.15s; background:var(--accent2); }
.hero-dot:nth-child(3) { animation-delay:0.3s; opacity:0.2; }

/* ══ CHAT MESSAGES ══ */
div[data-testid="stChatMessage"] {
    border-radius:16px !important; padding:18px 22px !important;
    margin-bottom:14px !important; box-shadow:var(--shadow-sm) !important;
    transition:all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    animation:messageSlideIn 0.4s cubic-bezier(0.22,1,0.36,1) both !important;
    position:relative; overflow:hidden;
}
div[data-testid="stChatMessage"]::before {
    content:''; position:absolute; top:0; left:0; width:3px; height:100%;
    background:linear-gradient(180deg, var(--accent), var(--accent2));
    opacity:0; transition:opacity 0.3s ease;
}
div[data-testid="stChatMessage"]:hover::before { opacity:1; }
div[data-testid="stChatMessage"]:nth-child(odd)  { background-color:var(--msg-user-bg)  !important; border:1px solid var(--msg-user-border) !important; }
div[data-testid="stChatMessage"]:nth-child(even) { background-color:var(--msg-ai-bg)    !important; border:1px solid var(--msg-ai-border)   !important; }
div[data-testid="stChatMessage"]:hover { transform:translateY(-2px) !important; box-shadow:var(--shadow-md) !important; }
div[data-testid="stChatMessage"] p { color:var(--text-primary) !important; line-height:1.75 !important; font-size:0.97rem; }

/* ══ CHAT INPUT ══ */
.stChatInputContainer {
    border-radius:16px !important; border:1.5px solid var(--border) !important;
    background-color:var(--input-bg) !important; box-shadow:var(--shadow-md) !important;
    transition:all 0.3s cubic-bezier(0.22,1,0.36,1) !important;
    animation:fadeInUp 0.5s ease 0.3s both;
}
.stChatInputContainer:focus-within {
    border-color:var(--accent) !important;
    box-shadow:var(--shadow-md), 0 0 0 4px rgba(74,124,247,0.12), var(--shadow-glow) !important;
    transform:translateY(-1px);
}
.stChatInputContainer textarea { color:var(--text-primary) !important; background:transparent !important; font-family:'DM Sans',sans-serif !important; font-size:0.97rem !important; }
.stChatInputContainer textarea::placeholder { color:var(--text-muted) !important; }

/* ══ FILE UPLOADER ══ */
.stFileUploader {
    background-color:var(--bg-surface-alt) !important; border-radius:12px !important;
    border:1.5px dashed var(--border) !important; padding:10px !important;
    transition:all 0.3s ease; animation:fadeInUp 0.4s ease 0.2s both;
}
.stFileUploader:hover { border-color:var(--accent) !important; box-shadow:0 0 0 3px rgba(74,124,247,0.08) !important; }
.stFileUploader label { color:var(--text-secondary) !important; font-size:0.82rem !important; }

/* ══ AVATARS ══ */
div[data-testid="stChatMessage"] img {
    border-radius:50% !important;
    border:2px solid var(--accent) !important;
    box-shadow:0 0 0 3px var(--accent-subtle), 0 0 12px var(--glow) !important;
    transition:all 0.3s ease;
}
div[data-testid="stChatMessage"]:hover img { box-shadow:0 0 0 3px var(--accent-subtle), 0 0 22px var(--glow) !important; transform:scale(1.1); }

/* ══ CODE BLOCKS ══ */
code { background-color:var(--bg-surface-alt) !important; color:var(--accent2) !important; border-radius:6px; padding:2px 7px; font-size:0.85em; border:1px solid var(--border); }
pre  { background-color:var(--bg-surface) !important; border:1px solid var(--border) !important; border-radius:12px !important; padding:16px !important; position:relative; overflow:hidden; }
pre::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg, var(--accent), var(--accent2)); }

/* ══ DIVIDER ══ */
hr { border:none !important; height:1px !important; background:linear-gradient(90deg, transparent, var(--border), transparent) !important; margin:18px 0 !important; }

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:10px; }
::-webkit-scrollbar-thumb:hover { background:var(--accent); box-shadow:0 0 6px var(--glow); }

/* ══ MISC ══ */
.stSpinner>div { border-top-color:var(--accent) !important; }
.stAlert { border-radius:12px !important; border:1px solid var(--border) !important; background-color:var(--bg-surface-alt) !important; animation:fadeInUp 0.4s ease both; }

/* ══ PARTICLES ══ */
.particles-wrap { position:fixed; top:0; left:0; right:0; bottom:0; pointer-events:none; z-index:0; overflow:hidden; }
.particle { position:absolute; border-radius:50%; background:var(--particle); animation:particleDrift linear infinite; }
</style>
""", unsafe_allow_html=True)

# ── Floating particles
st.markdown("""
<div class="particles-wrap">
  <div class="particle" style="left:8%;width:2px;height:2px;animation-duration:18s;animation-delay:0s;"></div>
  <div class="particle" style="left:20%;width:3px;height:3px;animation-duration:24s;animation-delay:3s;"></div>
  <div class="particle" style="left:35%;width:2px;height:2px;animation-duration:20s;animation-delay:6s;"></div>
  <div class="particle" style="left:52%;width:3px;height:3px;animation-duration:16s;animation-delay:1s;"></div>
  <div class="particle" style="left:67%;width:4px;height:4px;animation-duration:22s;animation-delay:9s;opacity:0.4;"></div>
  <div class="particle" style="left:78%;width:3px;height:3px;animation-duration:19s;animation-delay:4s;"></div>
  <div class="particle" style="left:90%;width:2px;height:2px;animation-duration:26s;animation-delay:7s;"></div>
  <div class="particle" style="left:44%;width:3px;height:3px;animation-duration:21s;animation-delay:12s;"></div>
  <div class="particle" style="left:60%;width:2px;height:2px;animation-duration:17s;animation-delay:5s;"></div>
</div>
""", unsafe_allow_html=True)


def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 3. SIDEBAR
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"

with st.sidebar:
    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;margin-bottom:22px;padding-top:4px;gap:11px;">
            <img src="data:image/png;base64,{logo_b64}" class="brand-logo-img" style="width:44px;">
            <span class="brand-name">HEXALOY</span>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div style="text-align:center;margin-bottom:22px;">
            <span class="brand-name">HEXALOY</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("＋  New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p class='history-label'>Chat History</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬  {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    uploaded_image = st.file_uploader("📸 Image Analysis (Optional)", type=['png', 'jpg', 'jpeg'])

    st.markdown("""
    <div class="signature-box">
        <p class="sig-label">Architected by</p>
        <p class="sig-name">VINIT MAAN</p>
        <p class="sig-version">Enterprise AI v6.0</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. MAIN AREA
# ==========================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">Intelligence Redefined</div>
    <h1 class="hero-title">HEXALOY <span class="accent-word">INTELLIGENCE</span></h1>
    <p class="hero-subtitle">Your Professional AI Assistant — Powered by Advanced Language Models</p>
    <div style="display:flex;justify-content:center;">
        <div class="status-badge"><span class="status-dot"></span>Systems Online</div>
    </div>
    <div class="hero-dots">
        <div class="hero-dot"></div>
        <div class="hero-dot"></div>
        <div class="hero-dot"></div>
    </div>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "user.png" if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# ==========================================
# 5. CHAT INPUT & STREAMING
# ==========================================
if prompt := st.chat_input("Ask Hexaloy anything..."):

    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Session") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:20] + "..."
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name

    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="user.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="logo.png"):
        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana"]):
            with st.spinner("Generating visualization..."):
                time.sleep(1.5)
                safe_prompt = urllib.parse.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
                st.image(img_url)
                st.session_state.sessions[st.session_state.current_chat].append(
                    {"role": "assistant", "content": f"![Generated Image]({img_url})"}
                )
        else:
            instructions = """
            You are 'HEXALOY', an exceptionally intelligent and professional AI assistant.
            1. You possess universal knowledge. You can answer ANY question about coding, science, history, daily life, or business perfectly.
            2. Keep your tone professional, highly accurate, and helpful. Use clear formatting.
            3. YOU ARE AN AI. Do not claim to be human.
            4. IF AND ONLY IF asked about your creator, owner, or who made you, reply exactly with: "I was architected and developed by VINIT MAAN."
            """

            try:
                def generate_response():
                    if uploaded_image:
                        base64_image = encode_image(uploaded_image)
                        stream = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": instructions},
                                {"role": "user", "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]}
                            ],
                            model="llama-3.2-11b-vision-preview",
                            temperature=0.7,
                            stream=True
                        )
                    else:
                        stream = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": instructions},
                                {"role": "user", "content": prompt}
                            ],
                            model="llama-3.3-70b-versatile",
                            temperature=0.7,
                            stream=True
                        )

                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            yield chunk.choices[0].delta.content

                response_text = st.write_stream(generate_response())
                st.session_state.sessions[st.session_state.current_chat].append(
                    {"role": "assistant", "content": response_text}
                )

            except Exception as e:
                st.error(f"System Fault: {str(e)}")
