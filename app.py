import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import time
import base64
import html
from groq import Groq

# ==========================================
# 1. PAGE CONFIG & SECRETS VALIDATION
# ==========================================
st.set_page_config(page_title="HEXALOY AI", page_icon="logo.png", layout="wide", initial_sidebar_state="expanded")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 System Error: GROQ_API_KEY is missing!")
    st.stop()

# ==========================================
# 2. CSS & STYLING
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FA; color: #1E293B; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stChatInputContainer { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; }
    .signature-box { margin-top: 40px; padding: 15px; border-radius: 8px; background: #F8F9FA; border: 1px solid #E2E8F0; text-align: center; }
    .signature-box p { margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase; }
    .signature-box h3 { margin: 5px 0 0 0; font-size: 1.1rem; color: #0F172A; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 3. SIDEBAR LOGIC
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"

with st.sidebar:
    # Logo Section
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 50px; margin-right: 12px;">
                <span style="font-size: 2.2rem; font-weight: 800; color: #2B5B9E;">HEXALOY</span>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='text-align:center;'>HEXALOY</h2>", unsafe_allow_html=True)

    if st.button("➕ New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()

    st.markdown("---")
    uploaded_image = st.file_uploader("📸 Image Analysis", type=['png', 'jpg', 'jpeg'])

    st.markdown("""
        <div class="signature-box">
            <p>Architected by</p>
            <h3>VINIT MAAN</h3>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. MAIN CHAT & AVIKA VOICE WIDGET (THE FIX)
# ==========================================
st.markdown("<h1 style='text-align: center;'>HEXALOY INTELLIGENCE</h1>", unsafe_allow_html=True)

# --- AVIKA VOICE WIDGET (BOTTOM-RIGHT FLOATING ICON) ---
if "VAPI_PUBLIC_KEY" in st.secrets and "VAPI_ASSISTANT_ID" in st.secrets:
    vapi_key = st.secrets["VAPI_PUBLIC_KEY"]
    vapi_id = st.secrets["VAPI_ASSISTANT_ID"]

    # Ye code widget ko right side mein floating banayega aur mic allow karega
    vapi_widget_html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <script src="https://cdn.jsdelivr.net/gh/VapiAI/html-widget@latest/dist/vapi-widget.js" defer></script>
        <script>
            window.addEventListener('load', function() {{
                window.vapiSDK.run({{
                    apiKey: "{vapi_key}",
                    assistantId: "{vapi_id}",
                    config: {{ position: "bottom-right", color: "#DC2626" }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    # Invisible iframe to bypass Streamlit restrictions
    st.components.v1.html(vapi_widget_html, height=0)
    st.markdown(f'<iframe srcdoc="{html.escape(vapi_widget_html)}" allow="microphone" style="display:none;"></iframe>', unsafe_allow_html=True)

# Chat History Display
for message in st.session_state.sessions[st.session_state.current_chat]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Hexaloy..."):
    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        if any(word in prompt.lower() for word in ["draw", "pic", "image"]):
            safe_prompt = urllib.parse.quote(prompt)
            img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
            st.image(img_url)
            st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": f"![Image]({img_url})"})
        else:
            instructions = "You are HEXALOY. Developed by VINIT MAAN."
            try:
                def generate():
                    stream = client.chat.completions.create(
                        messages=[{"role": "system", "content": instructions}, {"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                        stream=True
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                
                res = st.write_stream(generate())
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")
