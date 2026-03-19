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

VAPI_PUBLIC_KEY = st.secrets.get("VAPI_PUBLIC_KEY", "24cd89bd-9a4f-48d2-9566-26e861b9c4b5")
VAPI_ASSISTANT_ID = st.secrets.get("VAPI_ASSISTANT_ID", "5434184d-6893-4933-b90a-a4ce9eeac55a")

# ==========================================
# 2. CSS — AUTO DARK/LIGHT + SIDEBAR TOGGLE
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-primary: #F8FAFC;
    --bg-secondary: #FFFFFF;
    --bg-glass: rgba(255,255,255,0.72);
    --bg-sidebar: rgba(255,255,255,0.98);
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --accent: #2563EB;
    --accent-glow: rgba(37,99,235,0.15);
    --border: rgba(148,163,184,0.25);
    --border-solid: #E2E8F0;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
    --shadow-glow: 0 0 24px rgba(37,99,235,0.18);
    --input-bg: #FFFFFF;
    --scrollbar-thumb: #CBD5E1;
    --chat-odd: rgba(241,245,249,0.8);
    --chat-even: rgba(255,255,255,0.95);
    --toggle-bg: #FFFFFF;
    --toggle-border: #E2E8F0;
    --toggle-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0B0F1A;
        --bg-secondary: #111827;
        --bg-glass: rgba(17,24,39,0.80);
        --bg-sidebar: rgba(11,15,26,0.98);
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent: #3B82F6;
        --accent-glow: rgba(59,130,246,0.20);
        --border: rgba(255,255,255,0.08);
        --border-solid: rgba(255,255,255,0.10);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
        --shadow-glow: 0 0 24px rgba(59,130,246,0.25);
        --input-bg: #1E293B;
        --scrollbar-thumb: #334155;
        --chat-odd: rgba(17,24,39,0.80);
        --chat-even: rgba(30,41,59,0.60);
        --toggle-bg: #1E293B;
        --toggle-border: rgba(255,255,255,0.12);
        --toggle-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 7rem !important;
    max-width: 900px;
    margin: 0 auto;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 10px; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-solid) !important;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}
section[data-testid="stSidebar"] > div { padding: 20px 16px; }

/* SIDEBAR TOGGLE ARROW BUTTON */
.sidebar-toggle-btn {
    position: fixed;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    z-index: 9999;
    background: var(--toggle-bg);
    border: 1px solid var(--toggle-border);
    border-radius: 0 10px 10px 0;
    width: 22px;
    height: 56px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--toggle-shadow);
    transition: all 0.25s ease;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 700;
}
.sidebar-toggle-btn:hover {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
    width: 26px;
    box-shadow: var(--shadow-glow);
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: 1px solid transparent;
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
    cursor: pointer;
}
.stButton > button:hover {
    background: var(--accent-glow);
    color: var(--accent);
    border: 1px solid var(--accent-glow);
    transform: translateX(2px);
}
.new-chat-btn > div > button {
    background: linear-gradient(135deg, #2563EB, #1E40AF) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 20px !important;
    box-shadow: var(--shadow-glow) !important;
    text-align: center !important;
    justify-content: center !important;
    margin-bottom: 16px;
    transition: all 0.3s ease !important;
}
.new-chat-btn > div > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E3A8A) !important;
    box-shadow: 0 0 32px rgba(37,99,235,0.4) !important;
    transform: translateY(-1px) !important;
}

/* CHAT MESSAGES */
div[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 16px !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
    animation: fadeSlideIn 0.3s ease forwards;
}
div[data-testid="stChatMessage"]:nth-child(odd) {
    background: var(--chat-odd) !important;
    color: var(--text-primary) !important;
}
div[data-testid="stChatMessage"]:nth-child(even) {
    background: var(--chat-even) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-sm);
}
div[data-testid="stChatMessage"]:hover {
    border-color: var(--accent-glow) !important;
    box-shadow: var(--shadow-md);
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* CHAT INPUT */
.stChatInputContainer {
    border-radius: 16px !important;
    border: 1.5px solid var(--border-solid) !important;
    background: var(--input-bg) !important;
    box-shadow: var(--shadow-md) !important;
}
.stChatInputContainer:focus-within {
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-glow) !important;
}
.stChatInputContainer textarea {
    color: var(--text-primary) !important;
    background: transparent !important;
}

/* SIGNATURE BOX */
.signature-box {
    margin-top: 24px;
    padding: 14px;
    border-radius: 12px;
    background: var(--bg-glass);
    border: 1px solid var(--border-solid);
    text-align: center;
    backdrop-filter: blur(10px);
}
.signature-box p {
    margin: 0;
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}
.signature-box h3 {
    margin: 5px 0 2px 0;
    font-size: 1rem;
    color: var(--text-primary);
    font-weight: 800;
    letter-spacing: 1px;
}

.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 16px 0 8px 4px;
}
hr {
    border: none !important;
    border-top: 1px solid var(--border-solid) !important;
    margin: 16px 0 !important;
}

/* HERO */
.hero-title {
    font-size: 2.6rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 50%, #2563EB 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
@keyframes shimmer { to { background-position: 200% center; } }
.hero-sub {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 16px;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    color: #16A34A;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
}
@media (prefers-color-scheme: dark) { .status-badge { color: #4ADE80; } }
.pulse-dot {
    width: 7px; height: 7px;
    background: #22C55E;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.5; transform:scale(0.8); }
}

/* VOICE BUTTONS ROW */
.voice-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    margin: 14px 0 20px 0;
    flex-wrap: wrap;
}
.v-btn {
    background: var(--bg-glass);
    border: 1.5px solid var(--border-solid);
    border-radius: 50px;
    padding: 10px 22px;
    cursor: pointer;
    font-size: 0.84rem;
    font-weight: 600;
    color: var(--text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
    font-family: 'Inter', sans-serif;
}
.v-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: var(--shadow-glow);
    transform: translateY(-1px);
}
.v-btn.recording {
    background: rgba(239,68,68,0.1);
    border-color: #EF4444;
    color: #EF4444;
    animation: recordPulse 1s ease-in-out infinite;
}
.v-btn.vapi-active {
    background: rgba(124,58,237,0.1);
    border-color: #7C3AED;
    color: #7C3AED;
    animation: recordPulse 1s ease-in-out infinite;
}
@keyframes recordPulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.3); }
    50% { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
}

/* TYPING INDICATOR */
.typing-indicator { display:flex; align-items:center; gap:5px; padding:8px 0; }
.typing-dot {
    width:8px; height:8px;
    background: var(--accent);
    border-radius:50%;
    animation: typingBounce 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay:0.2s; }
.typing-dot:nth-child(3) { animation-delay:0.4s; }
@keyframes typingBounce {
    0%,60%,100% { transform:translateY(0); opacity:0.6; }
    30% { transform:translateY(-6px); opacity:1; }
}

/* WELCOME CARD */
.welcome-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    backdrop-filter: blur(16px);
    margin: 16px 0 28px 0;
}
.welcome-card h2 { font-size:1.25rem; font-weight:700; color:var(--text-primary); margin:10px 0 8px 0; }
.welcome-card p { color:var(--text-secondary); font-size:0.88rem; line-height:1.6; margin:0; }
.feature-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-top:16px; text-align:left; }
.feature-item {
    background: var(--bg-primary);
    border: 1px solid var(--border-solid);
    border-radius:10px;
    padding:11px 13px;
    font-size:0.82rem;
    color:var(--text-secondary);
    font-weight:500;
}
.feature-item span { font-size:1.05rem; margin-right:6px; }

/* VAPI STATUS BOX */
.vapi-status {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 0.82rem;
    color: #7C3AED;
    font-weight: 600;
    text-align: center;
    margin: 8px 0;
    display: none;
}
@media (prefers-color-scheme: dark) { .vapi-status { color: #A78BFA; } }

.active-chat > div > button {
    background: var(--accent-glow) !important;
    color: var(--accent) !important;
    border-color: var(--accent-glow) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. JS — SIDEBAR TOGGLE + BROWSER MIC + VAPI
# ==========================================
js_code = f"""
<script src="https://cdn.jsdelivr.net/npm/@vapi-ai/web@latest/dist/vapi.js"></script>

<script>
// ===== SIDEBAR TOGGLE =====
let sidebarVisible = true;

function toggleSidebar() {{
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    const toggleBtn = document.getElementById('sidebarToggle');
    if (!sidebar) return;
    
    if (sidebarVisible) {{
        sidebar.style.transform = 'translateX(-110%)';
        sidebar.style.transition = 'transform 0.3s ease';
        if (toggleBtn) {{ toggleBtn.innerHTML = '▶'; toggleBtn.style.left = '0px'; }}
        sidebarVisible = false;
    }} else {{
        sidebar.style.transform = 'translateX(0%)';
        sidebar.style.transition = 'transform 0.3s ease';
        if (toggleBtn) {{ toggleBtn.innerHTML = '◀'; toggleBtn.style.left = ''; }}
        sidebarVisible = true;
    }}
}}

// ===== BROWSER SPEECH RECOGNITION =====
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function startBrowserMic() {{
    if (!SpeechRecognition) {{
        alert("Voice input not supported. Please use Google Chrome.");
        return;
    }}
    const rec = new SpeechRecognition();
    rec.lang = 'hi-IN';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    const btn = document.getElementById('browserMicBtn');
    if (btn) {{ btn.classList.add('recording'); btn.innerHTML = '🔴 Sun raha hun...'; }}

    rec.start();

    rec.onresult = function(event) {{
        const transcript = event.results[0][0].transcript;
        const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (chatInput) {{
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(chatInput, transcript);
            chatInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            chatInput.focus();
        }}
    }};

    rec.onend = function() {{
        if (btn) {{ btn.classList.remove('recording'); btn.innerHTML = '🎤 Mic (Browser)'; }}
    }};

    rec.onerror = function(e) {{
        if (btn) {{ btn.classList.remove('recording'); btn.innerHTML = '🎤 Mic (Browser)'; }}
        if (e.error !== 'no-speech') alert('Voice error: ' + e.error);
    }};
}}

// ===== VAPI VOICE ASSISTANT =====
let vapiInstance = null;
let vapiCallActive = false;

async function startVapiCall() {{
    const btn = document.getElementById('vapiBtn');
    const statusBox = document.getElementById('vapiStatus');

    if (vapiCallActive) {{
        // Stop call
        if (vapiInstance) vapiInstance.stop();
        vapiCallActive = false;
        if (btn) {{ btn.classList.remove('vapi-active'); btn.innerHTML = '🤖 VAPI Voice Call'; }}
        if (statusBox) statusBox.style.display = 'none';
        return;
    }}

    try {{
        if (!vapiInstance) {{
            vapiInstance = new Vapi("{VAPI_PUBLIC_KEY}");

            vapiInstance.on('call-start', () => {{
                vapiCallActive = true;
                if (btn) {{ btn.classList.add('vapi-active'); btn.innerHTML = '🔴 Call Chal Rahi Hai (Band Karo)'; }}
                if (statusBox) {{ statusBox.style.display = 'block'; statusBox.innerHTML = '🟣 HEXALOY Agent se baat ho rahi hai...'; }}
            }});

            vapiInstance.on('call-end', () => {{
                vapiCallActive = false;
                if (btn) {{ btn.classList.remove('vapi-active'); btn.innerHTML = '🤖 VAPI Voice Call'; }}
                if (statusBox) statusBox.style.display = 'none';
            }});

            vapiInstance.on('message', (msg) => {{
                if (msg.type === 'transcript' && msg.transcriptType === 'final') {{
                    const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                    if (chatInput && msg.role === 'assistant') {{
                        // Show assistant reply in chat input area as info
                    }}
                }}
            }});

            vapiInstance.on('error', (e) => {{
                console.error('VAPI Error:', e);
                if (btn) {{ btn.classList.remove('vapi-active'); btn.innerHTML = '🤖 VAPI Voice Call'; }}
                if (statusBox) statusBox.style.display = 'none';
                vapiCallActive = false;
            }});
        }}

        await vapiInstance.start("{VAPI_ASSISTANT_ID}");

    }} catch(err) {{
        console.error('VAPI start error:', err);
        alert('VAPI Error: ' + err.message);
    }}
}}
</script>

<!-- SIDEBAR TOGGLE ARROW -->
<button class="sidebar-toggle-btn" id="sidebarToggle" onclick="toggleSidebar()" title="Sidebar Toggle">◀</button>

<!-- VOICE BUTTONS ROW -->
<div class="voice-row">
    <button class="v-btn" id="browserMicBtn" onclick="startBrowserMic()">🎤 Mic (Browser)</button>
    <button class="v-btn" id="vapiBtn" onclick="startVapiCall()">🤖 VAPI Voice Call</button>
</div>

<!-- VAPI STATUS -->
<div class="vapi-status" id="vapiStatus"></div>
"""

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 4. SESSION STATE
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
        logo_html = f"""
        <div style="display:flex;align-items:center;justify-content:center;margin-bottom:28px;padding-top:8px;">
            <img src="data:image/png;base64,{logo_base64}" style="width:46px;margin-right:12px;border-radius:10px;box-shadow:0 4px 12px rgba(37,99,235,0.25);">
            <span style="font-family:'Inter',sans-serif;font-size:2rem;font-weight:900;background:linear-gradient(135deg,#2563EB,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;">HEXALOY</span>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("<h2 style='color:#2563EB;font-weight:900;text-align:center;letter-spacing:2px;'>HEXALOY</h2>", unsafe_allow_html=True)

    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("➕  New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Chat History</div>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        is_active = chat_name == st.session_state.current_chat
        if is_active:
            st.markdown("<div class='active-chat'>", unsafe_allow_html=True)
        if st.button(f"💬  {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()
        if is_active:
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-label'>📸 Image Analysis</div>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload image (optional)", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if uploaded_image:
        st.image(uploaded_image, caption="Ready for analysis", use_container_width=True)

    st.markdown("""
        <div class="signature-box">
            <p>Architected by</p>
            <h3>VINIT MAAN</h3>
            <p style="font-size:0.62rem;margin-top:4px;letter-spacing:1px;">Enterprise AI v6.0</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. MAIN AREA
# ==========================================
st.markdown("<div class='hero-title'>HEXALOY INTELLIGENCE</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='hero-sub'>Your Professional AI Assistant</div>
    <div style='text-align:center;margin-bottom:20px;'>
        <span class='status-badge'><span class='pulse-dot'></span>&nbsp; System Online &middot; Enterprise AI v6.0</span>
    </div>
""", unsafe_allow_html=True)

current_messages = st.session_state.sessions[st.session_state.current_chat]

if len(current_messages) == 0:
    st.markdown("""
        <div class='welcome-card'>
            <div style='font-size:2.4rem;'>🧠</div>
            <h2>How can I help you today?</h2>
            <p>Ask me anything — coding, science, business, creative writing, image analysis, and more.<br>Ya seedha baat karo VAPI voice call se!</p>
            <div class='feature-grid'>
                <div class='feature-item'><span>💻</span>Code & Debug</div>
                <div class='feature-item'><span>🔬</span>Science & Research</div>
                <div class='feature-item'><span>🎨</span>Image Generation</div>
                <div class='feature-item'><span>🎤</span>Voice Input (Browser)</div>
                <div class='feature-item'><span>🤖</span>VAPI Voice Agent</div>
                <div class='feature-item'><span>🌐</span>Any Language</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# JS + SIDEBAR TOGGLE + VOICE BUTTONS
st.markdown(js_code, unsafe_allow_html=True)

# ==========================================
# 7. RENDER MESSAGES
# ==========================================
for message in current_messages:
    avatar_icon = "user.png" if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# ==========================================
# 8. CHAT INPUT & RESPONSE
# ==========================================
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

        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana", "generate image", "create image", "tasveer", "banao"]):
            with st.spinner("✨ Generating visualization..."):
                time.sleep(1.5)
                safe_prompt = urllib.parse.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
                st.image(img_url, use_container_width=True)
                st.session_state.sessions[st.session_state.current_chat].append({
                    "role": "assistant",
                    "content": f"![Generated Image]({img_url})"
                })
        else:
            instructions = """
            You are 'HEXALOY', an exceptionally intelligent and professional AI assistant created with Enterprise-grade precision.
            1. You possess universal knowledge. You can answer ANY question about coding, science, history, daily life, mathematics, or business with high accuracy.
            2. Keep your tone professional, accurate, and genuinely helpful. Use clean markdown formatting.
            3. YOU ARE AN AI. Never claim to be human.
            4. IF AND ONLY IF asked about your creator, owner, or who made you, reply exactly: "I was architected and developed by VINIT MAAN."
            5. When answering coding questions, always provide complete, runnable code with brief explanations.
            """

            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
            typing_placeholder.empty()

            try:
                def generate_response():
                    history = []
                    for msg in st.session_state.sessions[st.session_state.current_chat][:-1]:
                        history.append({"role": msg["role"], "content": msg["content"]})

                    if uploaded_image:
                        base64_image = encode_image(uploaded_image)
                        stream = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": instructions},
                                *history,
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
                                *history,
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
                st.session_state.sessions[st.session_state.current_chat].append({
                    "role": "assistant",
                    "content": response_text
                })

            except Exception as e:
                st.error(f"⚠️ System Fault: {str(e)}")
