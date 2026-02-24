import streamlit as st
import google.generativeai as genai
from groq import Groq
import urllib.parse
import time
import base64
import os

# ==========================================
# 1. DUAL HYBRID ENGINE SETUP
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("🚨 Gemini API Key missing in Secrets!")

if "GROQ_API_KEY" in st.secrets:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 Groq API Key missing in Secrets!")

st.set_page_config(page_title="HEXALOY AI", page_icon="💠", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. PROFESSIONAL LIGHT MODE UI
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FA; color: #1E293B; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    .stChatInputContainer { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; background-color: #FFFFFF !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    
    div[data-testid="stChatMessage"] { border-radius: 12px; padding: 15px 20px; margin-bottom: 20px; }
    div[data-testid="stChatMessage"]:nth-child(odd) { background-color: #F1F5F9 !important; border: 1px solid #E2E8F0 !important; color: #0F172A; }
    div[data-testid="stChatMessage"]:nth-child(even) { background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.02); color: #0F172A; }

    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    .stButton>button { width: 100%; text-align: left; background-color: transparent; border: 1px solid transparent; padding: 10px 15px; border-radius: 8px; font-weight: 500; color: #475569; transition: 0.2s; }
    .stButton>button:hover { background-color: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; }
    
    .new-chat-btn>div>button { background-color: #1A56A8; color: white; justify-content: center; font-weight: 600; margin-bottom: 20px; border-radius: 8px; }
    .new-chat-btn>div>button:hover { background-color: #134282; color: white; }

    .signature-box { margin-top: 40px; margin-bottom: 20px; padding: 15px; border-radius: 8px; background: #F8F9FA; border: 1px solid #E2E8F0; text-align: center; }
    .signature-box p { margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .signature-box h3 { margin: 5px 0 0 0; font-size: 1.1rem; color: #0F172A; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR WITH CUSTOM LOGO BRANDING
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"

with st.sidebar:
    # Read logo and perfectly align with matching Blue Hexaloy text
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
        
        logo_html = f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px; padding-top: 10px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 50px; margin-right: 12px;">
            <span style="font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 800; color: #2B5B9E; letter-spacing: 1.5px;">HEXALOY</span>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ logo.png not found. Upload it to GitHub!")
        st.markdown("<h3 style='color: #1A56A8; font-weight: 800; text-align: center;'>💠 HEXALOY</h3>", unsafe_allow_html=True)

    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("➕ New Session"):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='color: #64748B; font-size: 0.8rem; font-weight: 600; margin-top: 10px;'>Chat History</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("""
        <div class="signature-box">
            <p>Architected by</p>
            <h3>VINIT MAAN</h3>
            <p style="font-size: 0.6rem; margin-top: 5px;">Enterprise AI v6.0</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. MAIN CHAT & EXECUTION LOGIC
# ==========================================
st.markdown("<h1 style='color: #0F172A; font-weight: 800; text-align: center; font-size: 2.5rem;'>HEXALOY INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #64748B; font-weight: 500; margin-bottom: 30px; margin-top: -10px;'>Powered by Dual AI Engines</div>", unsafe_allow_html=True)

for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "🧑‍🎓" if message["role"] == "user" else "💠"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Hexaloy anything..."):
    
    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Session") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:20] + "..."
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name

    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="💠"):
        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana"]):
            with st.spinner("Rendering visualization..."):
                time.sleep(1.5)
                safe_prompt = urllib.parse.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
                st.image(img_url)
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": f"![Generated Image]({img_url})"})
        else:
            instructions = """
            You are 'HEXALOY', an exceptionally intelligent and professional AI assistant.
            1. You possess universal knowledge. You can answer ANY question perfectly.
            2. Keep your tone professional, highly accurate, and helpful. 
            3. YOU ARE AN AI. Do not claim to be human.
            4. IF AND ONLY IF asked about your creator, owner, or who made you, reply exactly with: "I was architected and developed by VINIT MAAN."
            """
            
            try:
                # Primary Engine: Google Gemini 1.5 Flash (Streaming)
                response = gemini_model.generate_content(f"{instructions}\n\nUser: {prompt}", stream=True)
                
                def stream_gemini():
                    for chunk in response:
                        yield chunk.text
                        time.sleep(0.02)
                
                full_res = st.write_stream(stream_gemini())
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                # Fallback Engine: Groq Llama 3.3
                st.warning("⚠️ Hexaloy Primary Core busy. Switching to Fallback Engine...")
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": instructions}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                full_res = chat_completion.choices[0].message.content
                st.markdown(full_res)
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": full_res})
