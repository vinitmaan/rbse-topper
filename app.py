import streamlit as st
import os
import urllib.parse
import time
import base64
from groq import Groq

# ==========================================
# 1. ENGINE SETUP (GROQ HIGH-SPEED)
# ==========================================
# API Key को सुरक्षित तरीके से सर्वर से निकालना
# os.environ की जगह अब हम st.secrets का इस्तेमाल करेंगे
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 API Key नहीं मिली! कृपया Secrets सेट करें।")
    st.stop()
client = Groq()

st.set_page_config(page_title="RBSE TOPPER AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. PREMIUM CSS (GEMINI CLONE + RED/GREEN THEME)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0B0F19; color: #E2E8F0; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    h1 { background: linear-gradient(90deg, #FF8A00, #E52E71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; text-align: center; padding-bottom: 5px; }
    
    .stChatInputContainer { border-radius: 25px !important; border: 1px solid #2A2F40 !important; background-color: #1E2230 !important; }
    
    div[data-testid="stChatMessage"] {
        border-radius: 15px; padding: 15px 20px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(145deg, #2D1115, #1A0A0C) !important; 
        border: 1px solid #FF4B4B !important;
    }
    
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(145deg, #0D2B1A, #081A10) !important; 
        border: 1px solid #00E676 !important;
    }

    section[data-testid="stSidebar"] { background-color: #131722; border-right: 1px solid #2A2F40; }
    
    .stButton>button { width: 100%; text-align: left; justify-content: flex-start; background-color: transparent; border: none; padding: 10px 15px; border-radius: 10px; font-weight: 500; transition: 0.2s; color: #94A3B8; }
    .stButton>button:hover { background-color: #1E2230; color: #E2E8F0; }
    
    .new-chat-btn>div>button { background: linear-gradient(90deg, #2A2F40, #1E2230); border: 1px solid #4A5568; color: white; justify-content: center; font-weight: 600; margin-bottom: 20px; }
    .new-chat-btn>div>button:hover { border: 1px solid #FF8A00; }

    /* FIX: Overlap Issue Solved. Changed to margin-top layout */
    .signature-box {
        margin-top: 40px; margin-bottom: 20px;
        padding: 15px; border-radius: 12px; background: rgba(30, 34, 48, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); text-align: center;
    }
    .signature-box p { margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .signature-box h3 { margin: 5px 0 0 0; font-size: 1.1rem; background: linear-gradient(90deg, #E2E8F0, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 3. MULTI-SESSION ARCHITECTURE (CHAT HISTORY)
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat 1"

# ==========================================
# 4. SIDEBAR (GEMINI CLONE)
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color: #E2E8F0; font-weight: 800;'>⚡ HEXALOY ENGINE</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("➕ New chat"):
        chat_id = f"New Chat {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='color: #64748B; font-size: 0.8rem; font-weight: 600; margin-top: 10px;'>Recent Chats</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()
            
    st.markdown("---")
    st.markdown("<p style='color: #64748B; font-size: 0.8rem; font-weight: 600;'>Tools</p>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("📸 Upload Photo", type=['png', 'jpg', 'jpeg'])

    st.markdown("""
        <div class="signature-box">
            <p>Architected & Engineered by</p>
            <h3>VINIT MAAN</h3>
            <p style="font-size: 0.6rem; margin-top: 5px;">RBSE Intelligence v5.0</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN CHAT INTERFACE
# ==========================================
st.title("🚀 RBSE TOPPER AI")
st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: -15px;'>Your Ultimate Study Master</p>", unsafe_allow_html=True)

for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "🧑‍🎓" if message["role"] == "user" else "👨‍🏫"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# ==========================================
# 6. EXECUTION LOGIC & GUARDRAILS
# ==========================================
if prompt := st.chat_input("Sawal pucho, ya likh 'Draw a pic of...'"):
    
    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Chat") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:20] + "..."
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name

    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="🧑‍🎓"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👨‍🏫"):
        chat_spinner = st.empty()
        
        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana"]):
            chat_spinner.info("🎨 Drawing your imagination...")
            time.sleep(1.5)
            safe_prompt = urllib.parse.quote(prompt)
            img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
            chat_spinner.empty()
            st.image(img_url)
            st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": f"![Generated Image]({img_url})"})
            
        else:
            chat_spinner.info("⚡ Master dimaag laga raha hai...")
            
            instructions = """
            CRITICAL RULES FOR YOUR IDENTITY:
            1. You are 'RBSE TOPPER AI', a highly intelligent teacher for Rajasthan Board students.
            2. YOU ARE AN AI. YOU ARE NEVER ALLOWED TO SAY "I AM VINIT MAAN". Do not claim to be a human.
            3. VINIT MAAN is your creator and developer. You are his creation.
            4. IF AND ONLY IF the user explicitly asks questions like "Who created you?", "Who made you?", "Tera malik kaun hai?", or "Who is your owner?", YOU MUST REPLY EXACTLY WITH: "Mujhe VINIT MAAN ne banaya hai."
            5. Always answer academic questions (Maths/Physics) step-by-step in a friendly Hinglish (Desi) tone.
            """
            
            try:
                if uploaded_image:
                    base64_image = encode_image(uploaded_image)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": instructions},
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                        temperature=0.5,
                    )
                else:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": instructions},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                    )
                
                response_text = chat_completion.choices[0].message.content
                chat_spinner.empty()
                st.write(response_text)
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                chat_spinner.empty()
                st.error(f"❌ System Fault: {str(e)}")