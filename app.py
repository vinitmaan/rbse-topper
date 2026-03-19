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
# 2. SYSTEM-AWARE DARK/LIGHT MODE CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* ---- CSS Variables: Light Mode ---- */
    :root {
        --bg-primary:       #F4F6FA;
        --bg-surface:       #FFFFFF;
        --bg-surface-alt:   #EEF2F8;
        --bg-sidebar:       #FFFFFF;
        --border:           #DDE3EF;
        --text-primary:     #0D1117;
        --text-secondary:   #5A6478;
        --text-muted:       #8E97AB;
        --accent:           #1B4FD8;
        --accent-hover:     #1440B8;
        --accent-subtle:    #EBF0FD;
        --msg-user-bg:      #F0F4FF;
        --msg-user-border:  #C7D4F8;
        --msg-ai-bg:        #FFFFFF;
        --msg-ai-border:    #DDE3EF;
        --input-bg:         #FFFFFF;
        --shadow-sm:        0 1px 4px rgba(0,0,0,0.06);
        --shadow-md:        0 4px 16px rgba(0,0,0,0.08);
        --badge-bg:         #1B4FD8;
        --badge-text:       #FFFFFF;
        --divider:          #E4E9F2;
    }

    /* ---- CSS Variables: Dark Mode ---- */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary:       #0D1117;
            --bg-surface:       #161B27;
            --bg-surface-alt:   #1C2333;
            --bg-sidebar:       #111622;
            --border:           #252E42;
            --text-primary:     #E8EDF5;
            --text-secondary:   #8B95AB;
            --text-muted:       #5A6478;
            --accent:           #4A7CF7;
            --accent-hover:     #3A6CE7;
            --accent-subtle:    #1A2545;
            --msg-user-bg:      #1A2545;
            --msg-user-border:  #2A3E72;
            --msg-ai-bg:        #161B27;
            --msg-ai-border:    #252E42;
            --input-bg:         #161B27;
            --shadow-sm:        0 1px 4px rgba(0,0,0,0.3);
            --shadow-md:        0 4px 16px rgba(0,0,0,0.4);
            --badge-bg:         #4A7CF7;
            --badge-text:       #FFFFFF;
            --divider:          #1E2840;
        }
    }

    /* ---- Global Reset ---- */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ---- Main Container ---- */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 900px;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem !important;
    }

    /* ---- Sidebar Buttons ---- */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: transparent;
        border: 1px solid transparent;
        padding: 9px 14px;
        border-radius: 9px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
        color: var(--text-secondary) !important;
        transition: all 0.18s ease;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: var(--bg-surface-alt) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
        transform: translateX(2px);
    }

    /* ---- New Session Button ---- */
    .new-chat-btn > div > button {
        background: linear-gradient(135deg, var(--accent), #5B8BFF) !important;
        color: #FFFFFF !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.5px;
        text-align: center !important;
        justify-content: center;
        border-radius: 10px !important;
        border: none !important;
        padding: 11px 20px !important;
        box-shadow: 0 4px 14px rgba(74, 124, 247, 0.35) !important;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease !important;
    }
    .new-chat-btn > div > button:hover {
        background: linear-gradient(135deg, var(--accent-hover), #4A7CF7) !important;
        box-shadow: 0 6px 20px rgba(74, 124, 247, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* ---- Chat Messages ---- */
    div[data-testid="stChatMessage"] {
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: var(--msg-user-bg) !important;
        border: 1px solid var(--msg-user-border) !important;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: var(--msg-ai-bg) !important;
        border: 1px solid var(--msg-ai-border) !important;
    }
    div[data-testid="stChatMessage"] p {
        color: var(--text-primary) !important;
        line-height: 1.7 !important;
    }
    div[data-testid="stChatMessage"]:hover {
        box-shadow: var(--shadow-md) !important;
    }

    /* ---- Chat Input ---- */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        background-color: var(--input-bg) !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.2s ease;
    }
    .stChatInputContainer:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(74, 124, 247, 0.15) !important;
    }
    .stChatInputContainer textarea {
        color: var(--text-primary) !important;
        background: transparent !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ---- File Uploader ---- */
    .stFileUploader {
        background-color: var(--bg-surface-alt) !important;
        border-radius: 10px !important;
        border: 1px dashed var(--border) !important;
        padding: 8px !important;
    }
    .stFileUploader label {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
    }

    /* ---- History Label ---- */
    .history-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 0 0 8px 4px;
    }

    /* ---- Signature Box ---- */
    .signature-box {
        margin-top: 32px;
        padding: 14px 16px;
        border-radius: 10px;
        background: var(--bg-surface-alt);
        border: 1px solid var(--border);
        text-align: center;
    }
    .signature-box .sig-label {
        margin: 0;
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'DM Sans', sans-serif;
    }
    .signature-box .sig-name {
        margin: 4px 0 0 0;
        font-size: 1rem;
        color: var(--text-primary);
        font-weight: 800;
        font-family: 'Syne', sans-serif;
        letter-spacing: 0.5px;
    }
    .signature-box .sig-version {
        margin: 3px 0 0 0;
        font-size: 0.6rem;
        color: var(--accent);
        letter-spacing: 1px;
        text-transform: uppercase;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
    }

    /* ---- Hero Title ---- */
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--text-primary);
        text-align: center;
        letter-spacing: -0.5px;
        line-height: 1;
        margin-bottom: 0;
    }
    .hero-title span {
        background: linear-gradient(135deg, var(--accent), #7BA7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 8px;
        margin-bottom: 32px;
        letter-spacing: 0.2px;
    }

    /* ---- Divider ---- */
    hr {
        border: none;
        border-top: 1px solid var(--divider) !important;
        margin: 16px 0 !important;
    }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* ---- Code blocks ---- */
    code {
        background-color: var(--bg-surface-alt) !important;
        color: var(--accent) !important;
        border-radius: 5px;
        padding: 2px 6px;
        font-size: 0.85em;
    }
    pre {
        background-color: var(--bg-surface-alt) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }

    /* ---- Spinner ---- */
    .stSpinner > div {
        border-top-color: var(--accent) !important;
    }

    /* ---- Error/Info ---- */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
        background-color: var(--bg-surface-alt) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 3. SIDEBAR WITH HEXALOY LOGO
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"

with st.sidebar:
    # Logo + Brand Name
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()

        logo_html = f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 22px; padding-top: 4px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 44px; margin-right: 11px; border-radius: 10px;">
            <span style="font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; color: var(--text-primary); letter-spacing: 2px;">HEXALOY</span>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div style='text-align:center; margin-bottom: 22px;'>
            <span style="font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; color: var(--text-primary); letter-spacing: 2px;">HEXALOY</span>
        </div>""", unsafe_allow_html=True)

    # New Session Button
    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("＋  New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat History
    st.markdown("<p class='history-label'>Chat History</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬  {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")

    # Image Upload
    uploaded_image = st.file_uploader("📸 Image Analysis (Optional)", type=['png', 'jpg', 'jpeg'])

    # Signature
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
st.markdown("<div class='hero-title'>HEXALOY <span>INTELLIGENCE</span></div>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Your Professional AI Assistant</p>", unsafe_allow_html=True)

# Chat History Display
for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "user.png" if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# ==========================================
# 5. CHAT INPUT & STREAMING LOGIC
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
                
