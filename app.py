import streamlit as st
import urllib.parse
import time, base64, os
from groq import Groq

# ── audio recorder (pip install audio-recorder-streamlit) ──
try:
    from audio_recorder_streamlit import audio_recorder
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False

# ════════════════════════════════════════════
# 1. PAGE CONFIG
# ════════════════════════════════════════════
st.set_page_config(
    page_title="HEXALOY AI",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "GROQ_API_KEY" not in st.secrets:
    st.error("🚨 GROQ_API_KEY missing in Streamlit Secrets!")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

VAPI_PUBLIC_KEY   = st.secrets.get("VAPI_PUBLIC_KEY",   "24cd89bd-9a4f-48d2-9566-26e861b9c4b5")
VAPI_ASSISTANT_ID = st.secrets.get("VAPI_ASSISTANT_ID", "5434184d-6893-4933-b90a-a4ce9eeac55a")

def b64(f): return base64.b64encode(f.getvalue()).decode()

# ════════════════════════════════════════════
# 2. SESSION STATE
# ════════════════════════════════════════════
def ss(k, v):
    if k not in st.session_state: st.session_state[k] = v

ss("sessions",     {"New Session": []})
ss("current_chat", "New Session")
ss("sidebar_open", True)
ss("vapi_active",  False)

# ════════════════════════════════════════════
# 3. CSS  (dark / light auto via prefers-color-scheme)
# ════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

/* ── tokens ── */
:root{
  --bg:#F0F2F8; --sur:#fff; --sb:#fff;
  --t1:#0D1117; --t2:#4A5568; --t3:#9AA5B4;
  --ac:#1847F5; --ac2:#6C2BD9;
  --gl:rgba(24,71,245,.14);
  --bd:rgba(0,0,0,.08); --bd2:rgba(0,0,0,.13);
  --cu:#EEF2FF; --ca:#fff;
  --inp:#fff;
  --sh:0 2px 14px rgba(0,0,0,.07);
  --sh2:0 8px 32px rgba(0,0,0,.11);
  --r:14px;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#070B14; --sur:#0F1623; --sb:#0A0F1C;
  --t1:#E8EDF5; --t2:#8B95A8; --t3:#4A5568;
  --ac:#4F80FF; --ac2:#9F6EFF;
  --gl:rgba(79,128,255,.18);
  --bd:rgba(255,255,255,.07); --bd2:rgba(255,255,255,.13);
  --cu:rgba(79,128,255,.09); --ca:rgba(255,255,255,.04);
  --inp:#111827;
  --sh:0 2px 14px rgba(0,0,0,.4);
  --sh2:0 8px 32px rgba(0,0,0,.5);
}}

/* ── base ── */
*{box-sizing:border-box;}
html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif!important;
  background:var(--bg)!important; color:var(--t1)!important;
}
#MainMenu,footer,header{visibility:hidden;}
.main .block-container{padding:1.5rem 1.8rem 8rem!important;max-width:880px;margin:0 auto;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:4px;}

/* ── sidebar ── */
section[data-testid="stSidebar"]{
  background:var(--sb)!important;
  border-right:1px solid var(--bd)!important;
}
section[data-testid="stSidebar"]>div{padding:18px 13px!important;}

/* ── sidebar collapse button (native Streamlit) ── */
button[data-testid="collapsedControl"],
button[kind="header"]{display:none!important;}   /* hide default arrow */

/* ── buttons ── */
.stButton>button{
  width:100%;text-align:left;background:transparent;
  border:1px solid transparent;padding:9px 13px;border-radius:10px;
  font-family:'DM Sans',sans-serif!important;font-weight:500;font-size:.84rem;
  color:var(--t2);transition:all .17s;cursor:pointer;
}
.stButton>button:hover{background:var(--gl);color:var(--ac);border-color:var(--gl);}

/* new-session button */
.nsb>div>button{
  background:linear-gradient(135deg,var(--ac),var(--ac2))!important;
  color:#fff!important;font-weight:700!important;border-radius:12px!important;
  border:none!important;text-align:center!important;
  box-shadow:0 0 18px var(--gl)!important;
  font-family:'DM Sans',sans-serif!important;
}
.nsb>div>button:hover{opacity:.9;transform:translateY(-1px)!important;}

/* active chat */
.ach>div>button{
  background:var(--gl)!important;color:var(--ac)!important;
  border-color:var(--gl)!important;font-weight:600!important;
}

/* sidebar toggle btn */
.tog>div>button{
  width:auto!important;background:transparent!important;
  border:1px solid var(--bd2)!important;border-radius:10px!important;
  color:var(--t2)!important;padding:7px 14px!important;
  font-size:.82rem!important;font-weight:600!important;
}
.tog>div>button:hover{background:var(--gl)!important;color:var(--ac)!important;}

/* ── chat messages ── */
div[data-testid="stChatMessage"]{
  border-radius:var(--r)!important;padding:14px 18px!important;
  margin-bottom:11px!important;border:1px solid var(--bd)!important;
  animation:fadeup .25s ease forwards;
}
div[data-testid="stChatMessage"]:nth-child(odd){background:var(--cu)!important;}
div[data-testid="stChatMessage"]:nth-child(even){background:var(--ca)!important;box-shadow:var(--sh);}
@keyframes fadeup{from{opacity:0;transform:translateY(7px);}to{opacity:1;transform:none;}}

/* ── chat input ── */
.stChatInputContainer{
  border-radius:16px!important;border:1.5px solid var(--bd2)!important;
  background:var(--inp)!important;box-shadow:var(--sh)!important;
}
.stChatInputContainer:focus-within{
  border-color:var(--ac)!important;
  box-shadow:0 0 0 3px var(--gl),var(--sh)!important;
}
.stChatInputContainer textarea{color:var(--t1)!important;background:transparent!important;}

/* ── file uploader ── */
.stFileUploader label{color:var(--t3)!important;font-size:.78rem!important;}

/* ── section label ── */
.sl{font-size:.67rem;font-weight:700;letter-spacing:1.7px;
    text-transform:uppercase;color:var(--t3);margin:16px 0 5px 2px;}

/* ── signature ── */
.sig{margin-top:28px;padding:13px;border-radius:12px;
     border:1px solid var(--bd);background:var(--bg);text-align:center;}
.sig p{font-size:.63rem;color:var(--t3);letter-spacing:1.4px;text-transform:uppercase;}
.sig h3{font-family:'Syne',sans-serif;font-size:.97rem;font-weight:800;
        color:var(--t1);letter-spacing:.4px;margin:4px 0 2px;}

/* ── hero ── */
.hero{text-align:center;padding:8px 0 6px;}
.hero h1{
  font-family:'Syne',sans-serif;font-weight:800;font-size:2.75rem;
  background:linear-gradient(135deg,var(--ac) 0%,var(--ac2) 55%,var(--ac) 100%);
  background-size:200%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 4s linear infinite;letter-spacing:-1px;line-height:1.1;
}
@keyframes shimmer{to{background-position:200%;}}
.hero p{color:var(--t2);font-size:.9rem;margin-top:6px;}

/* ── status pill ── */
.pill{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.22);
  color:#16A34A;border-radius:99px;padding:5px 14px;
  font-size:.73rem;font-weight:600;margin-top:10px;
}
@media(prefers-color-scheme:dark){.pill{color:#4ADE80;}}
.dot{width:7px;height:7px;border-radius:50%;background:#22C55E;
     animation:blink 1.6s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}

/* ── welcome card ── */
.wcard{
  background:var(--sur);border:1px solid var(--bd);
  border-radius:20px;padding:30px 26px;text-align:center;
  margin:18px 0 24px;box-shadow:var(--sh);
}
.wcard .ico{font-size:2.5rem;line-height:1;}
.wcard h2{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;margin:12px 0 8px;}
.wcard>p{color:var(--t2);font-size:.87rem;line-height:1.65;}
.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:18px;}
.fc{
  background:var(--bg);border:1px solid var(--bd);border-radius:11px;
  padding:12px 9px;font-size:.79rem;color:var(--t2);font-weight:500;
  transition:all .17s;cursor:default;
}
.fc:hover{border-color:var(--ac);color:var(--ac);background:var(--gl);}
.fc .fi{font-size:1.25rem;display:block;margin-bottom:5px;}

/* ── typing dots ── */
.typ{display:flex;align-items:center;gap:5px;padding:6px 2px;}
.td{width:8px;height:8px;border-radius:50%;background:var(--ac);
    animation:bnc 1.1s ease-in-out infinite;}
.td:nth-child(2){animation-delay:.18s;}.td:nth-child(3){animation-delay:.36s;}
@keyframes bnc{0%,60%,100%{transform:none;opacity:.5;}30%{transform:translateY(-6px);opacity:1;}}

/* ── voice row ── */
.vrow{display:flex;justify-content:center;align-items:center;
      gap:10px;margin:14px 0 20px;flex-wrap:wrap;}
.vbtn{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--sur);border:1.5px solid var(--bd2);
  border-radius:99px;padding:10px 22px;
  font-family:'DM Sans',sans-serif;font-size:.84rem;font-weight:600;
  color:var(--t2);cursor:pointer;transition:all .18s;box-shadow:var(--sh);
}
.vbtn:hover{border-color:var(--ac);color:var(--ac);box-shadow:0 0 16px var(--gl);}
.vbtn:active{transform:scale(.97);}

/* ── vapi status ── */
.vst{
  text-align:center;font-size:.81rem;font-weight:600;color:var(--ac2);
  padding:8px 16px;border-radius:10px;
  border:1px solid rgba(108,43,217,.22);background:rgba(108,43,217,.07);
  margin:4px auto 14px;max-width:380px;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# 4. SIDEBAR  (native Streamlit — always works)
# ════════════════════════════════════════════
with st.sidebar:
    # ── logo ──
    try:
        lb = base64.b64encode(open("logo.png","rb").read()).decode()
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;
                    margin-bottom:22px;padding-top:4px;">
          <img src="data:image/png;base64,{lb}"
               style="width:40px;margin-right:10px;border-radius:9px;
                      box-shadow:0 4px 12px var(--gl);">
          <span style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                       background:linear-gradient(135deg,var(--ac),var(--ac2));
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       background-clip:text;letter-spacing:2px;">HEXALOY</span>
        </div>""", unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='font-family:Syne,sans-serif;color:#1847F5;"
                    "text-align:center;'>HEXALOY</h2>", unsafe_allow_html=True)

    # ── new session ──
    st.markdown("<div class='nsb'>", unsafe_allow_html=True)
    if st.button("＋  New Session", key="nsb"):
        cid = f"Session {len(st.session_state.sessions)+1}"
        st.session_state.sessions[cid] = []
        st.session_state.current_chat  = cid
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── history ──
    st.markdown("<div class='sl'>Chat History</div>", unsafe_allow_html=True)
    for name in reversed(list(st.session_state.sessions.keys())):
        active = name == st.session_state.current_chat
        if active: st.markdown("<div class='ach'>", unsafe_allow_html=True)
        if st.button(f"💬  {name}", key=f"c_{name}"):
            st.session_state.current_chat = name
            st.rerun()
        if active: st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── image upload ──
    st.markdown("<div class='sl'>📸 Image Analysis</div>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("img", type=["png","jpg","jpeg"],
                                       label_visibility="collapsed")
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)

    st.markdown("---")

    # ── mic inside sidebar (audio_recorder_streamlit) ──
    st.markdown("<div class='sl'>🎙️ Voice to Text</div>", unsafe_allow_html=True)
    if AUDIO_OK:
        st.caption("Record karo → text chat mein aa jayega")
        audio_bytes = audio_recorder(
            text="",
            recording_color="#EF4444",
            neutral_color="#4F80FF",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=2.0,
            key="mic_rec"
        )
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.info("✅ Audio record hua! Groq Whisper se transcribe ho raha hai...")
            try:
                import io
                audio_file = io.BytesIO(audio_bytes)
                audio_file.name = "recording.wav"
                transcription = client.audio.transcriptions.create(
                    file=("recording.wav", audio_bytes),
                    model="whisper-large-v3",
                    response_format="text"
                )
                transcript_text = transcription if isinstance(transcription, str) else transcription.text
                st.success(f"📝 **Transcript:** {transcript_text}")
                # Save to session so main area can use it
                st.session_state["pending_voice"] = transcript_text
                st.rerun()
            except Exception as e:
                st.error(f"Transcription error: {e}")
    else:
        st.warning("Install karo: `pip install audio-recorder-streamlit`")

    # ── signature ──
    st.markdown("""
    <div class="sig">
      <p>Architected by</p>
      <h3>VINIT MAAN</h3>
      <p style="font-size:.6rem;margin-top:2px;">Enterprise AI v6.0</p>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# 5. TOP BAR  — sidebar toggle + title
# ════════════════════════════════════════════
tcol, hcol = st.columns([1, 9])
with tcol:
    arrow = "◀" if st.session_state.sidebar_open else "▶"
    st.markdown("<div class='tog'>", unsafe_allow_html=True)
    if st.button(arrow, key="sb_tog"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        # use CSS trick to hide sidebar
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# CSS injection to hide sidebar when toggled OFF
if not st.session_state.sidebar_open:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{display:none!important;}
    .main .block-container{max-width:100%!important;padding-left:2rem!important;}
    </style>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# 6. HERO
# ════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>HEXALOY INTELLIGENCE</h1>
  <p>Your Professional AI Assistant</p>
  <div><span class="pill"><span class="dot"></span>
       System Online &middot; Enterprise AI v6.0</span></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════
# 7. WELCOME CARD
# ════════════════════════════════════════════
msgs = st.session_state.sessions[st.session_state.current_chat]

if not msgs:
    st.markdown("""
    <div class="wcard">
      <div class="ico">🧠</div>
      <h2>How can I help you today?</h2>
      <p>Coding, science, business, creative writing, image analysis —<br>
         ya seedha VAPI voice call se baat karo!</p>
      <div class="fgrid">
        <div class="fc"><span class="fi">💻</span>Code & Debug</div>
        <div class="fc"><span class="fi">🔬</span>Science</div>
        <div class="fc"><span class="fi">🎨</span>Image Gen</div>
        <div class="fc"><span class="fi">🎤</span>Voice Input</div>
        <div class="fc"><span class="fi">🤖</span>VAPI Agent</div>
        <div class="fc"><span class="fi">🌐</span>Any Language</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# 8. VAPI BUTTON  (st.components — works in iframe)
# ════════════════════════════════════════════
import streamlit.components.v1 as components

vapi_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
  background:transparent;
  display:flex;justify-content:center;align-items:center;
  gap:12px;padding:4px 0 10px;flex-wrap:wrap;
  font-family:'DM Sans',sans-serif;
}}
.vbtn{{
  display:inline-flex;align-items:center;gap:8px;
  background:#ffffff;
  border:1.5px solid rgba(0,0,0,.13);
  border-radius:99px;padding:10px 22px;
  font-size:14px;font-weight:600;color:#4A5568;
  cursor:pointer;transition:all .18s;
  box-shadow:0 2px 10px rgba(0,0,0,.08);
  font-family:'DM Sans',sans-serif;
}}
.vbtn:hover{{border-color:#1847F5;color:#1847F5;
             box-shadow:0 0 16px rgba(24,71,245,.18);}}
.vbtn:active{{transform:scale(.97);}}
.vbtn.on{{
  border-color:#EF4444;color:#EF4444;
  background:rgba(239,68,68,.07);
  animation:rp 1s ease-in-out infinite;
}}
@keyframes rp{{
  0%,100%{{box-shadow:0 0 0 0 rgba(239,68,68,.3);}}
  50%{{box-shadow:0 0 0 8px rgba(239,68,68,0);}}
}}
#status{{
  text-align:center;font-size:12px;font-weight:600;
  color:#6C2BD9;padding:6px 14px;border-radius:8px;
  border:1px solid rgba(108,43,217,.2);background:rgba(108,43,217,.07);
  display:none;margin-top:6px;width:100%;
}}
@media(prefers-color-scheme:dark){{
  .vbtn{{background:#0F1623;border-color:rgba(255,255,255,.13);color:#8B95A8;
          box-shadow:0 2px 10px rgba(0,0,0,.4);}}
  .vbtn:hover{{border-color:#4F80FF;color:#4F80FF;box-shadow:0 0 16px rgba(79,128,255,.22);}}
  #status{{color:#9F6EFF;border-color:rgba(159,110,255,.22);background:rgba(159,110,255,.08);}}
}}
</style>
</head>
<body>
<button class="vbtn" id="vapiBtn" onclick="toggleVapi()">🤖 VAPI Voice Call</button>
<div id="status"></div>

<script src="https://cdn.jsdelivr.net/npm/@vapi-ai/web@latest/dist/vapi.umd.js"></script>
<script>
var vapi = null, on = false;

function toggleVapi() {{
  var btn = document.getElementById('vapiBtn');
  var sta = document.getElementById('status');

  if (on) {{
    if (vapi) vapi.stop();
    on = false;
    btn.classList.remove('on');
    btn.innerHTML = '🤖 VAPI Voice Call';
    sta.style.display = 'none';
    return;
  }}

  function tryStart() {{
    if (typeof Vapi === 'undefined') {{ setTimeout(tryStart, 300); return; }}
    if (!vapi) {{
      vapi = new Vapi('{VAPI_PUBLIC_KEY}');
      vapi.on('call-start', function() {{
        on = true;
        btn.classList.add('on');
        btn.innerHTML = '🔴 Call Chal Rahi Hai — Band Karo';
        sta.style.display = 'block';
        sta.innerHTML = '🟣 Hexaloy Agent se live baat ho rahi hai...';
      }});
      vapi.on('call-end', function() {{
        on = false;
        btn.classList.remove('on');
        btn.innerHTML = '🤖 VAPI Voice Call';
        sta.style.display = 'none';
      }});
      vapi.on('error', function(e) {{
        on = false;
        btn.classList.remove('on');
        btn.innerHTML = '🤖 VAPI Voice Call';
        sta.style.display = 'none';
        console.error(e);
      }});
    }}
    vapi.start('{VAPI_ASSISTANT_ID}');
  }}
  tryStart();
}}
</script>
</body>
</html>
"""
components.html(vapi_html, height=80, scrolling=False)

# ════════════════════════════════════════════
# 9. RENDER CHAT MESSAGES
# ════════════════════════════════════════════
for m in msgs:
    av = "user.png" if m["role"] == "user" else "logo.png"
    with st.chat_message(m["role"], avatar=av):
        st.markdown(m["content"])

# ════════════════════════════════════════════
# 10. HANDLE PENDING VOICE TRANSCRIPT
# ════════════════════════════════════════════
pending = st.session_state.pop("pending_voice", None)

# ════════════════════════════════════════════
# 11. CHAT INPUT
# ════════════════════════════════════════════
prompt = st.chat_input("Ask Hexaloy anything...") or pending

if prompt:
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

        IMAGE_KW = ["draw","pic","image","photo bana","generate image",
                    "create image","tasveer","banao","picture"]
        if any(w in prompt.lower() for w in IMAGE_KW):
            with st.spinner("✨ Generating image..."):
                time.sleep(1.1)
                url = ("https://image.pollinations.ai/prompt/"
                       + urllib.parse.quote(prompt)
                       + "?width=800&height=420&nologo=true")
                st.image(url, use_container_width=True)
            st.session_state.sessions[cur].append(
                {"role":"assistant","content":f"![img]({url})"})
        else:
            SYS = (
                "You are HEXALOY — an exceptionally intelligent enterprise AI.\n"
                "1. Answer any question perfectly: coding, science, history, maths, business.\n"
                "2. Use clean markdown: headers, bullets, code blocks where needed.\n"
                "3. You are an AI. Never claim to be human.\n"
                "4. If asked who made you: 'I was architected and developed by VINIT MAAN.'\n"
                "5. For code questions: complete, runnable code + brief explanation.\n"
                "6. Be precise and concise."
            )
            history = [{"role":m["role"],"content":m["content"]}
                       for m in st.session_state.sessions[cur][:-1]]

            ph = st.empty()
            ph.markdown('<div class="typ"><div class="td"></div>'
                        '<div class="td"></div><div class="td"></div></div>',
                        unsafe_allow_html=True)
            time.sleep(0.4)
            ph.empty()

            try:
                def stream():
                    if uploaded_image:
                        resp = client.chat.completions.create(
                            messages=[{"role":"system","content":SYS},*history,
                                      {"role":"user","content":[
                                          {"type":"text","text":prompt},
                                          {"type":"image_url","image_url":{
                                              "url":f"data:image/jpeg;base64,{b64(uploaded_image)}"}}]}],
                            model="llama-3.2-11b-vision-preview",
                            temperature=0.7, stream=True)
                    else:
                        resp = client.chat.completions.create(
                            messages=[{"role":"system","content":SYS},*history,
                                      {"role":"user","content":prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=0.7, stream=True)
                    for chunk in resp:
                        c = chunk.choices[0].delta.content
                        if c: yield c

                out = st.write_stream(stream())
                st.session_state.sessions[cur].append({"role":"assistant","content":out})
            except Exception as e:
                st.error(f"⚠️ {e}")
