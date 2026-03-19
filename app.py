import streamlit as st
import urllib.parse
import time
import base64
from groq import Groq

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="HEXALOY AI",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🚨 GROQ_API_KEY missing in Streamlit Secrets!")
    st.stop()

VAPI_PUBLIC_KEY    = st.secrets.get("VAPI_PUBLIC_KEY",    "24cd89bd-9a4f-48d2-9566-26e861b9c4b5")
VAPI_ASSISTANT_ID  = st.secrets.get("VAPI_ASSISTANT_ID",  "5434184d-6893-4933-b90a-a4ce9eeac55a")

def encode_image(f):
    return base64.b64encode(f.getvalue()).decode("utf-8")

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "sessions"     not in st.session_state:
    st.session_state.sessions     = {"New Session": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Session"
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# ─────────────────────────────────────────
# FULL CSS
# ─────────────────────────────────────────
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── TOKENS ─────────────────────────────── */
:root{
  --bg:       #F0F2F7;
  --surface:  #FFFFFF;
  --sidebar:  #FFFFFF;
  --txt:      #0D1117;
  --txt2:     #4A5568;
  --txt3:     #9AA5B4;
  --acc:      #1847F5;
  --acc2:     #6C2BD9;
  --acc-glow: rgba(24,71,245,.18);
  --bdr:      rgba(0,0,0,.08);
  --bdr2:     rgba(0,0,0,.12);
  --chat-u:   #EEF2FF;
  --chat-a:   #FFFFFF;
  --inp:      #FFFFFF;
  --shadow:   0 2px 12px rgba(0,0,0,.08);
  --shadow2:  0 8px 32px rgba(0,0,0,.12);
  --radius:   14px;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:      #070B14;
    --surface: #0F1623;
    --sidebar: #0A0F1C;
    --txt:     #E8EDF5;
    --txt2:    #8B95A8;
    --txt3:    #4A5568;
    --acc:     #4F80FF;
    --acc2:    #9F6EFF;
    --acc-glow:rgba(79,128,255,.20);
    --bdr:     rgba(255,255,255,.07);
    --bdr2:    rgba(255,255,255,.12);
    --chat-u:  rgba(79,128,255,.10);
    --chat-a:  rgba(255,255,255,.04);
    --inp:     #111827;
    --shadow:  0 2px 12px rgba(0,0,0,.4);
    --shadow2: 0 8px 32px rgba(0,0,0,.5);
  }
}

/* ── RESET ───────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif!important;
  background:var(--bg)!important;
  color:var(--txt)!important;
}
#MainMenu,footer,header{visibility:hidden;}

/* ── MAIN CONTAINER ──────────────────────── */
.main .block-container{
  padding:2rem 2rem 8rem!important;
  max-width:860px;
  margin:0 auto;
}

/* ── SCROLLBAR ───────────────────────────── */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:var(--bdr2);border-radius:4px;}

/* ── SIDEBAR ─────────────────────────────── */
section[data-testid="stSidebar"]{
  background:var(--sidebar)!important;
  border-right:1px solid var(--bdr)!important;
}
section[data-testid="stSidebar"]>div{padding:20px 14px!important;}

/* ── STREAMLIT BUTTONS (sidebar) ─────────── */
.stButton>button{
  width:100%;text-align:left;
  background:transparent;
  border:1px solid transparent;
  padding:9px 13px;
  border-radius:10px;
  font-family:'DM Sans',sans-serif;
  font-weight:500;font-size:.84rem;
  color:var(--txt2);
  transition:all .18s;
}
.stButton>button:hover{
  background:var(--acc-glow);
  color:var(--acc);
  border-color:var(--acc-glow);
}
/* new session button */
div[data-testid="stButton"].new-session-btn button,
.nsb>div>button{
  background:linear-gradient(135deg,var(--acc),var(--acc2))!important;
  color:#fff!important;font-weight:700!important;
  border-radius:12px!important;border:none!important;
  padding:11px!important;text-align:center!important;
  box-shadow:0 0 20px var(--acc-glow)!important;
  font-family:'DM Sans',sans-serif!important;
}

/* ── CHAT MESSAGES ───────────────────────── */
div[data-testid="stChatMessage"]{
  border-radius:var(--radius)!important;
  padding:14px 18px!important;
  margin-bottom:12px!important;
  border:1px solid var(--bdr)!important;
  animation:fadeUp .28s ease forwards;
}
div[data-testid="stChatMessage"]:nth-child(odd){background:var(--chat-u)!important;}
div[data-testid="stChatMessage"]:nth-child(even){background:var(--chat-a)!important;box-shadow:var(--shadow);}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}

/* ── CHAT INPUT ──────────────────────────── */
.stChatInputContainer{
  border-radius:16px!important;
  border:1.5px solid var(--bdr2)!important;
  background:var(--inp)!important;
  box-shadow:var(--shadow)!important;
}
.stChatInputContainer:focus-within{
  border-color:var(--acc)!important;
  box-shadow:0 0 0 3px var(--acc-glow),var(--shadow)!important;
}
.stChatInputContainer textarea{color:var(--txt)!important;background:transparent!important;}

/* ── FILE UPLOADER ───────────────────────── */
.stFileUploader{background:transparent!important;}

/* ── ACTIVE SIDEBAR ITEM ─────────────────── */
.active-chat>div>button{
  background:var(--acc-glow)!important;
  color:var(--acc)!important;
  border-color:var(--acc-glow)!important;
  font-weight:600!important;
}

/* ── SECTION LABEL ───────────────────────── */
.slabel{
  font-size:.68rem;font-weight:700;letter-spacing:1.6px;
  text-transform:uppercase;color:var(--txt3);
  margin:18px 0 6px 2px;
}

/* ── SIGNATURE ───────────────────────────── */
.sig{
  margin-top:auto;padding:14px;
  border-radius:12px;
  border:1px solid var(--bdr);
  text-align:center;
  background:var(--bg);
}
.sig p{font-size:.65rem;color:var(--txt3);letter-spacing:1.4px;text-transform:uppercase;}
.sig h3{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--txt);letter-spacing:.5px;margin:4px 0 2px;}

/* ── HERO ────────────────────────────────── */
.hero{text-align:center;padding:10px 0 6px;}
.hero h1{
  font-family:'Syne',sans-serif;font-weight:800;font-size:2.8rem;
  background:linear-gradient(135deg,var(--acc) 0%,var(--acc2) 60%,var(--acc) 100%);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 4s linear infinite;
  letter-spacing:-1px;line-height:1.1;
}
@keyframes shimmer{to{background-position:200%;}}
.hero p{color:var(--txt2);font-size:.92rem;margin-top:6px;}

/* ── STATUS PILL ─────────────────────────── */
.pill{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.22);
  color:#16A34A;border-radius:99px;padding:5px 14px;
  font-size:.73rem;font-weight:600;margin-top:10px;
}
@media(prefers-color-scheme:dark){.pill{color:#4ADE80;}}
.dot{width:7px;height:7px;border-radius:50%;background:#22C55E;animation:blink 1.6s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}

/* ── WELCOME CARD ────────────────────────── */
.wcard{
  background:var(--surface);border:1px solid var(--bdr);
  border-radius:20px;padding:32px 28px;
  text-align:center;margin:20px 0 26px;
  box-shadow:var(--shadow);
}
.wcard .big{font-size:2.6rem;line-height:1;}
.wcard h2{font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:700;margin:12px 0 8px;}
.wcard>p{color:var(--txt2);font-size:.88rem;line-height:1.65;}
.fgrid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  margin-top:20px;
}
.fc{
  background:var(--bg);border:1px solid var(--bdr);
  border-radius:12px;padding:13px 10px;
  font-size:.8rem;color:var(--txt2);font-weight:500;
  cursor:default;transition:all .18s;
}
.fc:hover{border-color:var(--acc);color:var(--acc);background:var(--acc-glow);}
.fc .ico{font-size:1.3rem;display:block;margin-bottom:5px;}

/* ── TYPING ──────────────────────────────── */
.typing{display:flex;align-items:center;gap:5px;padding:6px 0;}
.td{
  width:8px;height:8px;border-radius:50%;background:var(--acc);
  animation:bounce 1.1s ease-in-out infinite;
}
.td:nth-child(2){animation-delay:.18s;}
.td:nth-child(3){animation-delay:.36s;}
@keyframes bounce{0%,60%,100%{transform:none;opacity:.55;}30%{transform:translateY(-6px);opacity:1;}}

/* ── VOICE BUTTONS ───────────────────────── */
.vrow{
  display:flex;justify-content:center;align-items:center;
  gap:10px;margin:16px 0 22px;flex-wrap:wrap;
}
.vbtn{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--surface);border:1.5px solid var(--bdr2);
  border-radius:99px;padding:10px 22px;
  font-family:'DM Sans',sans-serif;font-size:.84rem;font-weight:600;
  color:var(--txt2);cursor:pointer;transition:all .2s;
  box-shadow:var(--shadow);
}
.vbtn:hover{border-color:var(--acc);color:var(--acc);box-shadow:0 0 18px var(--acc-glow);}
.vbtn:active{transform:scale(.97);}
.vbtn.rec{border-color:#EF4444;color:#EF4444;background:rgba(239,68,68,.08);animation:recpulse 1s ease-in-out infinite;}
.vbtn.vcall-on{border-color:var(--acc2);color:var(--acc2);background:rgba(108,43,217,.08);animation:recpulse 1s ease-in-out infinite;}
@keyframes recpulse{
  0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,.3);}
  50%{box-shadow:0 0 0 7px rgba(239,68,68,0);}
}

/* ── VAPI STATUS ─────────────────────────── */
.vstatus{
  text-align:center;font-size:.82rem;font-weight:600;color:var(--acc2);
  padding:8px 16px;border-radius:10px;
  border:1px solid rgba(108,43,217,.2);background:rgba(108,43,217,.07);
  margin:0 auto 12px;display:none;max-width:400px;
}

/* ── SIDEBAR TOGGLE ──────────────────────── */
/* Pure Streamlit button in sidebar — styled as pill */
.tog-wrap>div>button{
  background:linear-gradient(90deg,var(--acc),var(--acc2))!important;
  color:#fff!important;font-weight:700!important;
  border-radius:99px!important;border:none!important;
  padding:8px 18px!important;font-size:.8rem!important;
  width:auto!important;
  box-shadow:0 0 12px var(--acc-glow)!important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# VAPI + MIC JS  (injected once, works globally)
# ─────────────────────────────────────────
VAPI_JS = f"""
<script>
(function(){{
  // ── load Vapi SDK ──
  if(!window.__vapiLoaded){{
    var s=document.createElement('script');
    s.src='https://cdn.jsdelivr.net/npm/@vapi-ai/web@latest/dist/vapi.umd.js';
    s.onload=function(){{window.__vapiLoaded=true;}};
    document.head.appendChild(s);
  }}

  // ── helpers ──
  function chatTextarea(){{
    return window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
  }}
  function setTA(val){{
    var ta=chatTextarea();
    if(!ta) return;
    var setter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
    setter.call(ta,val);
    ta.dispatchEvent(new Event('input',{{bubbles:true}}));
    ta.focus();
  }}

  // ── Browser Mic ──
  window.hexStartMic=function(){{
    var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!SR){{alert('Chrome browser use karo mic ke liye!');return;}}
    var r=new SR();
    r.lang='hi-IN';r.interimResults=false;r.maxAlternatives=1;
    var btn=document.getElementById('hxMicBtn');
    if(btn){{btn.classList.add('rec');btn.innerHTML='&#128308; Sun raha hun...';}}
    r.start();
    r.onresult=function(e){{ setTA(e.results[0][0].transcript); }};
    r.onend=function(){{if(btn){{btn.classList.remove('rec');btn.innerHTML='&#127908; Mic Input';}}}};
    r.onerror=function(e){{
      if(btn){{btn.classList.remove('rec');btn.innerHTML='&#127908; Mic Input';}}
      if(e.error!=='no-speech')alert('Mic error: '+e.error);
    }};
  }};

  // ── VAPI Call ──
  var vapi=null,callOn=false;
  window.hexVapiToggle=function(){{
    var btn=document.getElementById('hxVapiBtn');
    var sta=document.getElementById('hxVapiStatus');
    if(callOn){{
      if(vapi)vapi.stop();
      callOn=false;
      if(btn){{btn.classList.remove('vcall-on');btn.innerHTML='&#129302; VAPI Voice Call';}}
      if(sta)sta.style.display='none';
      return;
    }}
    function doStart(){{
      if(typeof Vapi==='undefined'){{setTimeout(doStart,300);return;}}
      if(!vapi){{
        vapi=new Vapi('{VAPI_PUBLIC_KEY}');
        vapi.on('call-start',function(){{
          callOn=true;
          if(btn){{btn.classList.add('vcall-on');btn.innerHTML='&#128308; Call Chal Rahi Hai — Band Karo';}}
          if(sta){{sta.style.display='block';sta.innerHTML='&#128995; Hexaloy Agent se baat ho rahi hai...';}};
        }});
        vapi.on('call-end',function(){{
          callOn=false;
          if(btn){{btn.classList.remove('vcall-on');btn.innerHTML='&#129302; VAPI Voice Call';}}
          if(sta)sta.style.display='none';
        }});
        vapi.on('error',function(e){{
          console.error('VAPI:',e);
          callOn=false;
          if(btn){{btn.classList.remove('vcall-on');btn.innerHTML='&#129302; VAPI Voice Call';}}
          if(sta)sta.style.display='none';
        }});
      }}
      vapi.start('{VAPI_ASSISTANT_ID}');
    }}
    doStart();
  }};
}})();
</script>
"""

VOICE_HTML = """
<div class="vrow">
  <button class="vbtn" id="hxMicBtn" onclick="hexStartMic()">🎤 Mic Input</button>
  <button class="vbtn" id="hxVapiBtn" onclick="hexVapiToggle()">🤖 VAPI Voice Call</button>
</div>
<div class="vstatus" id="hxVapiStatus"></div>
"""

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    # Logo
    try:
        logo_b64 = base64.b64encode(open("logo.png","rb").read()).decode()
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;margin-bottom:24px;padding-top:6px;">
          <img src="data:image/png;base64,{logo_b64}"
               style="width:42px;margin-right:11px;border-radius:10px;box-shadow:0 4px 14px var(--acc-glow);">
          <span style="font-family:'Syne',sans-serif;font-size:1.85rem;font-weight:800;
                       background:linear-gradient(135deg,var(--acc),var(--acc2));
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       background-clip:text;letter-spacing:2px;">HEXALOY</span>
        </div>""", unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='font-family:Syne,sans-serif;color:#1847F5;text-align:center;'>HEXALOY</h2>",
                    unsafe_allow_html=True)

    # New Session
    st.markdown("<div class='nsb'>", unsafe_allow_html=True)
    if st.button("＋  New Session", key="new_sess"):
        cid = f"Session {len(st.session_state.sessions)+1}"
        st.session_state.sessions[cid] = []
        st.session_state.current_chat  = cid
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # History
    st.markdown("<div class='slabel'>Chat History</div>", unsafe_allow_html=True)
    for name in reversed(list(st.session_state.sessions.keys())):
        active = name == st.session_state.current_chat
        if active: st.markdown("<div class='active-chat'>", unsafe_allow_html=True)
        if st.button(f"💬  {name}", key=f"chat_{name}"):
            st.session_state.current_chat = name
            st.rerun()
        if active: st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='slabel'>📸 Image Analysis</div>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("img", type=["png","jpg","jpeg"],
                                       label_visibility="collapsed")
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)

    # Signature
    st.markdown("""
    <div class="sig">
      <p>Architected by</p>
      <h3>VINIT MAAN</h3>
      <p style="font-size:.6rem;margin-top:3px;">Enterprise AI v6.0</p>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR TOGGLE — Streamlit native button
# ─────────────────────────────────────────
# We use a small col trick to put toggle at top-left
tog_col, _ = st.columns([1, 11])
with tog_col:
    icon = "☰" if not st.session_state.sidebar_open else "✕"
    # Use JS to actually toggle; Python state just tracks
    pass  # handled via JS below

# Inject VAPI js + sidebar toggle js
st.markdown(VAPI_JS, unsafe_allow_html=True)

# Floating sidebar toggle button via HTML/JS
SIDEBAR_TOGGLE_JS = """
<script>
(function(){
  function getSidebar(){
    return window.parent.document.querySelector('section[data-testid="stSidebar"]');
  }
  function getToggleBtn(){
    return document.getElementById('hxSbToggle');
  }
  var open=true;
  window.hexToggleSidebar=function(){
    var sb=getSidebar();
    var btn=getToggleBtn();
    if(!sb) return;
    if(open){
      sb.style.cssText='transform:translateX(-110%);transition:transform .3s cubic-bezier(.4,0,.2,1);';
      if(btn){ btn.innerHTML='&#9776;'; btn.style.left='6px'; }
      open=false;
    } else {
      sb.style.cssText='transform:translateX(0);transition:transform .3s cubic-bezier(.4,0,.2,1);';
      if(btn){ btn.innerHTML='&#10005;'; btn.style.left=''; }
      open=true;
    }
  };
})();
</script>

<style>
#hxSbToggle{
  position:fixed;
  top:14px;
  right:18px;
  z-index:99999;
  width:38px;height:38px;
  border-radius:50%;
  background:linear-gradient(135deg,#1847F5,#6C2BD9);
  border:none;cursor:pointer;
  font-size:16px;color:#fff;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 4px 16px rgba(24,71,245,.35);
  transition:all .2s;
}
#hxSbToggle:hover{
  transform:scale(1.1);
  box-shadow:0 6px 22px rgba(24,71,245,.5);
}
@media(prefers-color-scheme:dark){
  #hxSbToggle{box-shadow:0 4px 16px rgba(79,128,255,.4);}
}
</style>
<button id="hxSbToggle" onclick="hexToggleSidebar()" title="Toggle Sidebar">✕</button>
"""
st.markdown(SIDEBAR_TOGGLE_JS, unsafe_allow_html=True)

# ─────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>HEXALOY INTELLIGENCE</h1>
  <p>Your Professional AI Assistant</p>
  <div><span class="pill"><span class="dot"></span>System Online &middot; Enterprise AI v6.0</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# WELCOME CARD (only when no messages)
# ─────────────────────────────────────────
msgs = st.session_state.sessions[st.session_state.current_chat]

if not msgs:
    st.markdown("""
    <div class="wcard">
      <div class="big">🧠</div>
      <h2>How can I help you today?</h2>
      <p>Ask me anything — coding, science, business, creative writing,<br>image analysis. Ya VAPI se seedha baat karo!</p>
      <div class="fgrid">
        <div class="fc"><span class="ico">💻</span>Code & Debug</div>
        <div class="fc"><span class="ico">🔬</span>Science</div>
        <div class="fc"><span class="ico">🎨</span>Image Gen</div>
        <div class="fc"><span class="ico">🎤</span>Voice Input</div>
        <div class="fc"><span class="ico">🤖</span>VAPI Agent</div>
        <div class="fc"><span class="ico">🌐</span>Any Language</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# VOICE BUTTONS
# ─────────────────────────────────────────
st.markdown(VOICE_HTML, unsafe_allow_html=True)

# ─────────────────────────────────────────
# RENDER MESSAGES
# ─────────────────────────────────────────
for m in msgs:
    av = "user.png" if m["role"] == "user" else "logo.png"
    with st.chat_message(m["role"], avatar=av):
        st.markdown(m["content"])

# ─────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────
if prompt := st.chat_input("Ask Hexaloy anything..."):

    # rename New Session
    cur = st.session_state.current_chat
    if cur.startswith("New Session") and not msgs:
        nn = prompt[:24].strip() + "…"
        st.session_state.sessions[nn] = st.session_state.sessions.pop(cur)
        st.session_state.current_chat  = nn
        cur = nn

    st.session_state.sessions[cur].append({"role":"user","content":prompt})
    with st.chat_message("user", avatar="user.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="logo.png"):

        IMAGE_WORDS = ["draw","pic","image","photo bana","generate image",
                       "create image","tasveer","banao","picture"]
        if any(w in prompt.lower() for w in IMAGE_WORDS):
            with st.spinner("✨ Generating..."):
                time.sleep(1.2)
                img_url = (
                    "https://image.pollinations.ai/prompt/"
                    + urllib.parse.quote(prompt)
                    + "?width=800&height=420&nologo=true"
                )
                st.image(img_url, use_container_width=True)
            st.session_state.sessions[cur].append(
                {"role":"assistant","content":f"![img]({img_url})"})

        else:
            SYS = """You are HEXALOY — an exceptionally intelligent enterprise AI assistant.
1. Answer any question: coding, science, history, maths, business — perfectly.
2. Use clean markdown: headers, bullet points, code blocks where helpful.
3. You are an AI. Never claim to be human.
4. If asked who made you: "I was architected and developed by VINIT MAAN."
5. For code questions: provide complete, runnable code with brief explanation.
6. Be precise, professional, and concise."""

            # typing animation
            ph = st.empty()
            ph.markdown('<div class="typing"><div class="td"></div><div class="td"></div><div class="td"></div></div>',
                        unsafe_allow_html=True)
            time.sleep(0.45)
            ph.empty()

            history = [{"role":m["role"],"content":m["content"]}
                       for m in st.session_state.sessions[cur][:-1]]

            try:
                def stream():
                    if uploaded_image:
                        b64 = encode_image(uploaded_image)
                        resp = client.chat.completions.create(
                            messages=[{"role":"system","content":SYS},
                                      *history,
                                      {"role":"user","content":[
                                          {"type":"text","text":prompt},
                                          {"type":"image_url","image_url":{
                                              "url":f"data:image/jpeg;base64,{b64}"}}]}],
                            model="llama-3.2-11b-vision-preview",
                            temperature=0.7, stream=True)
                    else:
                        resp = client.chat.completions.create(
                            messages=[{"role":"system","content":SYS},
                                      *history,
                                      {"role":"user","content":prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=0.7, stream=True)
                    for chunk in resp:
                        c = chunk.choices[0].delta.content
                        if c: yield c

                out = st.write_stream(stream())
                st.session_state.sessions[cur].append({"role":"assistant","content":out})

            except Exception as e:
                st.error(f"⚠️ System Fault: {e}")
