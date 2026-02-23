import streamlit as st
import os
import urllib.parse
import time
import base64
from groq import Groq

# ==========================================
# 1. ENGINE SETUP & SECRETS
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    # Fallback for local testing if secrets aren't set locally
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", api_key = st.secrets["GROQ_API_KEY"]))

st.set_page_config(page_title="RBSE TOPPER AI", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. PROFESSIONAL LIGHT MODE CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FA; color: #1E293B; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* Clean Professional Header */
    h1 { color: #0F172A; font-weight: 800; text-align: center; padding-bottom: 5px; font-size: 2.5rem; }
    .subtitle { text-align: center; color: #64748B; margin-top: -15px; font-weight: 500; margin-bottom: 30px;}
    
    /* Input Bar */
    .stChatInputContainer { border-radius: 12px !important; border: 1px solid #CBD5E1 !important; background-color: #FFFFFF !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    
    /* =========================================
       CLEAN CHAT BUBBLES
       ========================================= */
    div[data-testid="stChatMessage"] {
        border-radius: 12px; padding: 15px 20px; margin-bottom: 20px;
    }
    
    /* User (Student) - Light Gray */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #F1F5F9 !important; 
        border: 1px solid #E2E8F0 !important;
        color: #0F172A;
    }
    
    /* Master (AI) - Pure White with subtle shadow */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #FFFFFF !important; 
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        color: #0F172A;
    }

    /* =========================================
       PROFESSIONAL SIDEBAR
       ========================================= */
    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    
    .stButton>button { width: 100%; text-align: left; justify-content: flex-start; background-color: transparent; border: 1px solid transparent; padding: 10px 15px; border-radius: 8px; font-weight: 500; color: #475569; transition: 0.2s; }
    .stButton>button:hover { background-color: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; }
    
    /* Highlighted New Chat Button */
    .new-chat-btn>div>button { background-color: #0F172A; color: white; justify-content: center; font-weight: 600; margin-bottom: 20px; border-radius: 8px; }
    .new-chat-btn>div>button:hover { background-color: #1E293B; color: white; }

    /* Clean Signature Box */
    .signature-box {
        margin-top: 40px; margin-bottom: 20px;
        padding: 15px; border-radius: 8px; background: #F8F9FA; border: 1px solid #E2E8F0; text-align: center;
    }
    .signature-box p { margin: 0; font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .signature-box h3 { margin: 5px 0 0 0; font-size: 1.1rem; color: #0F172A; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 3. STATE MANAGEMENT
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat 1"

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color: #0F172A; font-weight: 800; text-align: center;'>🎓 HEXALOY AI</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("➕ New Session"):
        chat_id = f"New Chat {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='color: #64748B; font-size: 0.8rem; font-weight: 600; margin-top: 10px;'>Chat History</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()
            
    st.markdown("---")
    uploaded_image = st.file_uploader("📸 Image Analysis (Optional)", type=['png', 'jpg', 'jpeg'])

    st.markdown("""
        <div class="signature-box">
            <p>Architected by</p>
            <h3>VINIT MAAN</h3>
            <p style="font-size: 0.6rem; margin-top: 5px;">Enterprise AI v6.0</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN CHAT UI
# ==========================================
st.markdown("<h1>RBSE TOPPER AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your Professional AI Assistant</div>", unsafe_allow_html=True)

for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🎓"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# ==========================================
# 6. EXECUTION & STREAMING LOGIC
# ==========================================
if prompt := st.chat_input("Ask me anything..."):
    
    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Chat") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:20] + "..."
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name

    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="🧑‍🎓"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎓"):
        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana"]):
            with st.spinner("Generating visualization..."):
                time.sleep(1.5)
                safe_prompt = urllib.parse.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
                st.image(img_url)
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": f"![Generated Image]({img_url})"})
        else:
            instructions = """
            You are 'RBSE TOPPER AI', an exceptionally intelligent and professional AI assistant.
            1. You possess universal knowledge. You can answer ANY question about coding, science, history, daily life, or business perfectly.
            2. Keep your tone professional, highly accurate, and helpful. Use clear formatting (bullet points, bold text).
            3. YOU ARE AN AI. Do not claim to be human.
            4. IF AND ONLY IF asked about your creator, owner, or who made you, reply exactly with: "I was architected and developed by VINIT MAAN."
            """
            
            try:
                # Streaming Output Generator
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

                # Execute Stream and write to screen smoothly
                response_text = st.write_stream(generate_response())
                
                # Save to history
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"System Fault: {str(e)}")
