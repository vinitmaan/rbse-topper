import streamlit as st
import urllib.parse
import time
import base64
from groq import Groq

# ==========================================
# 1. PAGE CONFIG & SECRETS VALIDATION
# ==========================================
st.set_page_config(page_title="HEXALOY AI", page_icon="logo.png", layout="wide", initial_sidebar_state="expanded")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 System Error: GROQ_API_KEY is missing in Streamlit Secrets!")
    st.stop()

# ==========================================
# 2. PREMIUM DARK UI CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --bg-primary: #080C14;
        --bg-secondary: #0D1320;
        --bg-card: #111827;
        --bg-glass: rgba(255, 255, 255, 0.04);
        --border: rgba(255, 255, 255, 0.07);
        --border-hover: rgba(99, 179, 237, 0.3);
        --accent: #3B82F6;
        --accent-glow: rgba(59, 130, 246, 0.15);
        --accent-2: #06B6D4;
        --text-primary: #F1F5F9;
        --text-secondary: #64748B;
        --text-muted: #334155;
        --user-bubble: #1E3A5F;
        --ai-bubble: #111827;
        --success: #10B981;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── MAIN BACKGROUND ── */
    .stApp {
        background: var(--bg-primary) !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59, 130, 246, 0.08), transparent),
            radial-gradient(ellipse 40% 30% at 80% 80%, rgba(6, 182, 212, 0.05), transparent) !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
        backdrop-filter: blur(20px);
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 20px;
    }

    /* ── SIDEBAR BUTTONS ── */
    .stButton > button {
        width: 100%;
        text-align: left;
        background: var(--bg-glass) !important;
        border: 1px solid var(--border) !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease !important;
        margin-bottom: 4px !important;
    }
    .stButton > button:hover {
        background: var(--accent-glow) !important;
        border-color: var(--border-hover) !important;
        color: var(--text-primary) !important;
        transform: translateX(3px);
    }

    /* ── NEW SESSION BUTTON ── */
    .new-chat-btn > div > button {
        background: linear-gradient(135deg, #1D4ED8, #0284C7) !important;
        color: #fff !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
        border: none !important;
        border-radius: 10px !important;
        text-align: center !important;
        padding: 12px !important;
        box-shadow: 0 4px 20px rgba(29, 78, 216, 0.35) !important;
        transition: all 0.25s ease !important;
        margin-bottom: 18px !important;
    }
    .new-chat-btn > div > button:hover {
        background: linear-gradient(135deg, #2563EB, #0EA5E9) !important;
        box-shadow: 0 6px 28px rgba(29, 78, 216, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* ── CHAT MESSAGES ── */
    div[data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 18px 22px !important;
        margin-bottom: 16px !important;
        border: 1px solid var(--border) !important;
        backdrop-filter: blur(10px);
        animation: fadeSlideIn 0.3s ease forwards;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.5), rgba(17, 24, 39, 0.6)) !important;
        border-color: rgba(59, 130, 246, 0.12) !important;
        color: var(--text-primary) !important;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(17, 24, 39, 0.7) !important;
        border-color: var(--border) !important;
        color: var(--text-primary) !important;
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── CHAT INPUT ── */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 1px solid var(--border-hover) !important;
        background: var(--bg-card) !important;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.08), 0 4px 20px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(20px);
    }
    .stChatInputContainer textarea {
        background: transparent !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stChatInputContainer textarea::placeholder {
        color: var(--text-muted) !important;
    }

    /* ── FILE UPLOADER ── */
    .stFileUploader {
        background: var(--bg-glass) !important;
        border: 1px dashed var(--border-hover) !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }
    .stFileUploader label {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
    }

    /* ── DIVIDER ── */
    hr {
        border-color: var(--border) !important;
        margin: 16px 0 !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }

    /* ── SPINNER ── */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* ── SECTION LABEL ── */
    .section-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 14px 0 8px 4px;
    }

    /* ── SIGNATURE BOX ── */
    .signature-box {
        margin-top: 30px;
        padding: 14px 16px;
        border-radius: 12px;
        background: var(--bg-glass);
        border: 1px solid var(--border);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .signature-box::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent), var(--accent-2), transparent);
    }
    .signature-box .label {
        font-size: 0.62rem;
        font-family: 'Syne', sans-serif;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .signature-box .name {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 1px;
    }
    .signature-box .version {
        font-size: 0.58rem;
        color: var(--text-muted);
        margin-top: 4px;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 1px;
    }

    /* ── MAIN HEADER ── */
    .main-header {
        text-align: center;
        padding: 40px 0 10px 0;
        position: relative;
    }
    .main-header .badge {
        display: inline-block;
        background: var(--accent-glow);
        border: 1px solid rgba(59, 130, 246, 0.25);
        color: #60A5FA;
        font-family: 'Syne', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 100px;
        margin-bottom: 16px;
    }
    .main-header h1 {
        font-family: 'Syne', sans-serif !important;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #F1F5F9 30%, #60A5FA 70%, #06B6D4) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-bottom: 10px;
    }
    .main-header p {
        color: var(--text-secondary) !important;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        margin-bottom: 32px;
    }

    /* ── LOGO AREA ── */
    .logo-area {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px 0 24px 0;
        gap: 12px;
    }
    .logo-area img {
        width: 42px;
        height: 42px;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }
    .logo-area .brand {
        font-family: 'Syne', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 3px;
    }

    /* ── GLOW DIVIDER ── */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0.3;
        margin: 8px 0 20px 0;
        border: none;
    }
    </style>
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
    # Logo
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
        <div class="logo-area">
            <img src="data:image/png;base64,{logo_base64}">
            <span class="brand">HEXALOY</span>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="logo-area">
            <span class="brand">HEXALOY</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # New Session Button
    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("＋  New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat History
    st.markdown("<div class='section-label'>Chat History</div>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬  {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")

    # Image Upload
    st.markdown("<div class='section-label'>Image Analysis</div>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded_image:
        st.markdown(f"<p style='font-size:0.75rem; color:#10B981; margin-top:6px;'>✓ Image ready</p>", unsafe_allow_html=True)

    # Signature
    st.markdown("""
        <div class="signature-box">
            <div class="label">Architected by</div>
            <div class="name">VINIT MAAN</div>
            <div class="version">Enterprise AI · v6.0</div>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. MAIN CHAT AREA
# ==========================================
st.markdown("""
    <div class="main-header">
        <div class="badge">⬡ Intelligence Platform</div>
        <h1>HEXALOY INTELLIGENCE</h1>
        <p>Your Professional AI Assistant — Ask anything, get expert answers</p>
    </div>
""", unsafe_allow_html=True)

# Render chat history
for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "user.png" if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Hexaloy anything..."):

    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Session") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:22] + "..."
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
