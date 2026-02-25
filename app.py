import streamlit as st
import urllib.parse
import time
import base64
from groq import Groq

# ==========================================
# 1. PAGE CONFIGURATION (Must be first)
# ==========================================
st.set_page_config(page_title="HEXALOY", page_icon="logo.png", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. ENGINE SETUP (STABLE & SECURE)
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 System Error: Groq API Key is missing in Streamlit Secrets!")
    st.stop()

# ==========================================
# 3. MINIMALIST SaaS CSS (Clean Look)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #FFFFFF; color: #1E293B; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Clean Input Bar */
    .stChatInputContainer { border-radius: 8px !important; border: 1px solid #E2E8F0 !important; background-color: #FFFFFF !important; box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important; padding-bottom: 20px !important;}
    
    /* Clean Chat Bubbles */
    div[data-testid="stChatMessage"] { padding: 1.5rem; background-color: transparent; border: none; }
    div[data-testid="stChatMessage"]:nth-child(odd) { background-color: #FFFFFF !important; border-bottom: 1px solid #F1F5F9 !important; }
    div[data-testid="stChatMessage"]:nth-child(even) { background-color: #F8FAFC !important; border-bottom: 1px solid #F1F5F9 !important; }
    
    /* Clean Sidebar */
    section[data-testid="stSidebar"] { background-color: #F9F9F9; border-right: 1px solid #E5E5E5; }
    .stButton>button { width: 100%; text-align: left; background-color: transparent; border: 1px solid transparent; padding: 8px 12px; border-radius: 6px; font-weight: 500; color: #333; }
    .stButton>button:hover { background-color: #EAEAEA; }
    .new-chat-btn>div>button { background-color: #FFFFFF; border: 1px solid #D1D5DB; color: #111827; justify-content: center; font-weight: 500; margin-bottom: 15px; }
    .new-chat-btn>div>button:hover { background-color: #F3F4F6; }
    </style>
    """, unsafe_allow_html=True)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ==========================================
# 4. STATE MANAGEMENT
# ==========================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# ==========================================
# 5. CLEAN SIDEBAR
# ==========================================
with st.sidebar:
    # Logo Alignment
    try:
        with open("logo.png", "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 30px; padding-top: 10px;">
            <img src="data:image/png;base64,{logo_base64}" style="width: 32px; margin-right: 10px;">
            <span style="font-size: 1.3rem; font-weight: 600; color: #111827; letter-spacing: 0.5px;">HEXALOY</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.markdown("<h3 style='color: #111827; font-weight: 600; margin-bottom: 30px;'>logo.png HEXALOY</h3>", unsafe_allow_html=True)

    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)
    if st.button("📝 New chat"):
        chat_id = f"Chat {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.75rem; color: #6B7280; font-weight: 600; margin-bottom: 5px;'>History</p>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.sessions.keys())):
        if st.button(f"{chat_name}", key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    uploaded_image = st.file_uploader("Attach Image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# ==========================================
# 6. CHAT EXECUTION
# ==========================================
for message in st.session_state.sessions[st.session_state.current_chat]:
    avatar_icon = "🧑‍💻" if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Hexaloy..."):
    
    curr_chat = st.session_state.current_chat
    if curr_chat.startswith("New Chat") and len(st.session_state.sessions[curr_chat]) == 0:
        new_name = prompt[:20] + "..."
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name

    st.session_state.sessions[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="💠"): 
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="logo.png"):
        if any(word in prompt.lower() for word in ["draw", "pic", "image", "photo bana"]):
            with st.spinner("Generating image..."):
                safe_prompt = urllib.parse.quote(prompt)
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=400&nologo=true"
                st.image(img_url)
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": f"![Generated Image]({img_url})"})
        else:
            instructions = """
            You are 'HEXALOY', a professional, highly intelligent AI assistant.
            1. Keep your tone concise, direct, and factual.
            2. Use markdown formatting for clarity.
            3. Do not use excessive emojis or filler words.
            4. If asked about your creator, reply: "I was architected and developed by VINIT MAAN."
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
                st.session_state.sessions[st.session_state.current_chat].append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
