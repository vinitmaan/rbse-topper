import streamlit as st
import os
import urllib.parse
import time
import base64
import json
import random
import re
import hashlib
import datetime
import io
from groq import Groq

# ══════════════════════════════════════════════════════════════════════════════
#   HEXALOY AI — ENTERPRISE INTELLIGENCE PLATFORM v7.0
#   Architected by VINIT MAAN | Engineered for Supremacy
# ══════════════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1: ENGINE SETUP
# ──────────────────────────────────────────────────────────────────────────────
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
   client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(
    page_title="HEXALOY AI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2: MEGA CSS — LIGHT THEME, ANIMATIONS, GLASSMORPHISM, EVERYTHING
# ──────────────────────────────────────────────────────────────────────────────
MEGA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ════════════════════════════════════════
   ROOT VARIABLES
════════════════════════════════════════ */
:root {
    --bg-primary:     #F0F4FF;
    --bg-secondary:   #FFFFFF;
    --bg-tertiary:    #E8EEFF;
    --bg-card:        rgba(255, 255, 255, 0.85);
    --bg-glass:       rgba(255, 255, 255, 0.60);

    --blue-100:       #EEF2FF;
    --blue-200:       #C7D7FF;
    --blue-300:       #93AEFF;
    --blue-400:       #5B7CFF;
    --blue-500:       #2B5CE6;
    --blue-600:       #1A3FCC;
    --blue-700:       #0F27A3;

    --navy:           #0D1B4B;
    --navy-lt:        #1E2F6E;

    --accent-gold:    #F5A623;
    --accent-teal:    #0FBFBF;
    --accent-coral:   #FF6B6B;
    --accent-green:   #22C55E;
    --accent-purple:  #8B5CF6;

    --text-primary:   #0D1B4B;
    --text-secondary: #3B4B7E;
    --text-muted:     #7A8BB0;
    --text-light:     #AAB4CC;

    --border:         rgba(43, 92, 230, 0.15);
    --border-strong:  rgba(43, 92, 230, 0.30);
    --shadow-sm:      0 2px 8px rgba(43, 92, 230, 0.08);
    --shadow-md:      0 8px 32px rgba(43, 92, 230, 0.12);
    --shadow-lg:      0 20px 60px rgba(43, 92, 230, 0.16);
    --shadow-xl:      0 32px 80px rgba(43, 92, 230, 0.20);

    --radius-sm:      8px;
    --radius-md:      14px;
    --radius-lg:      20px;
    --radius-xl:      28px;
    --radius-full:    999px;

    --transition:     all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
    --transition-fast:all 0.16s ease;
    --transition-slow:all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ════════════════════════════════════════
   GLOBAL RESET & BASE
════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body {
    background: var(--bg-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
    scroll-behavior: smooth;
}

#MainMenu, footer, header { visibility: hidden !important; }

/* Animated mesh background */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%,   rgba(93,124,255,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(15,191,191,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 60% 40%,  rgba(245,166,35,0.05) 0%, transparent 60%),
        linear-gradient(160deg, #F0F4FF 0%, #E8EEFF 50%, #F4F0FF 100%);
    z-index: -2;
    pointer-events: none;
}

/* Floating orbs */
body::after {
    content: '';
    position: fixed;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(43,92,230,0.06) 0%, transparent 70%);
    top: -200px; right: -200px;
    animation: float-orb 8s ease-in-out infinite alternate;
    z-index: -1;
    pointer-events: none;
}

@keyframes float-orb {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(-60px, 80px) scale(1.15); }
}

/* ════════════════════════════════════════
   STREAMLIT OVERRIDES
════════════════════════════════════════ */
.main .block-container {
    padding: 0 2rem 4rem 2rem !important;
    max-width: 100% !important;
}

/* ════════════════════════════════════════
   SIDEBAR
════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.92) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 40px rgba(43,92,230,0.07) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ════════════════════════════════════════
   LOGO HEADER
════════════════════════════════════════ */
.hexaloy-logo-wrap {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(135deg, rgba(43,92,230,0.04) 0%, rgba(15,191,191,0.03) 100%);
    position: relative;
    overflow: hidden;
}

.hexaloy-logo-wrap::before {
    content: '';
    position: absolute;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(43,92,230,0.12) 0%, transparent 70%);
    top: -40px; right: -20px;
}

.hexaloy-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: var(--navy) !important;
    letter-spacing: 2px;
    margin: 0;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--blue-600), var(--accent-teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hexaloy-subtitle {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: var(--radius-full);
    font-size: 0.7rem;
    font-weight: 600;
    color: #16A34A;
    margin-top: 10px;
    letter-spacing: 0.5px;
}

.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #22C55E;
    animation: status-pulse 2s ease-in-out infinite;
}

@keyframes status-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
    50%       { box-shadow: 0 0 0 4px rgba(34,197,94,0); }
}

/* ════════════════════════════════════════
   SIDEBAR NAV SECTIONS
════════════════════════════════════════ */
.sidebar-section-title {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--text-light);
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 18px 24px 8px;
    margin: 0;
}

/* ════════════════════════════════════════
   NEW SESSION BUTTON
════════════════════════════════════════ */
.new-session-area {
    padding: 16px 16px 0;
}

div[data-testid="stButton"].new-chat-btn > div > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--blue-500) 0%, var(--blue-600) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 13px 20px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
    box-shadow: 0 4px 20px rgba(43,92,230,0.30) !important;
    position: relative;
    overflow: hidden;
}

div[data-testid="stButton"].new-chat-btn > div > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 50%);
    border-radius: inherit;
}

div[data-testid="stButton"].new-chat-btn > div > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(43,92,230,0.40) !important;
    background: linear-gradient(135deg, var(--blue-400) 0%, var(--blue-500) 100%) !important;
}

div[data-testid="stButton"].new-chat-btn > div > button:active {
    transform: translateY(0px) scale(0.98) !important;
}

/* ════════════════════════════════════════
   CHAT HISTORY BUTTONS
════════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 14px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-align: left !important;
    cursor: pointer !important;
    transition: var(--transition-fast) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

.stButton > button:hover {
    background: var(--blue-100) !important;
    color: var(--blue-500) !important;
    border-color: var(--border) !important;
}

/* ════════════════════════════════════════
   ACTIVE CHAT INDICATOR
════════════════════════════════════════ */
.active-chat button {
    background: linear-gradient(135deg, var(--blue-100) 0%, rgba(15,191,191,0.08) 100%) !important;
    color: var(--blue-600) !important;
    border-color: var(--border-strong) !important;
    font-weight: 600 !important;
}

/* ════════════════════════════════════════
   MODEL SELECTOR
════════════════════════════════════════ */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
    backdrop-filter: blur(12px);
    transition: var(--transition-fast) !important;
}

.stSelectbox > div > div:hover {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 3px rgba(43,92,230,0.10) !important;
}

/* ════════════════════════════════════════
   SLIDERS
════════════════════════════════════════ */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--blue-500), var(--accent-teal)) !important;
}

.stSlider > div > div > div > div > div {
    background: var(--blue-500) !important;
    border: 2px solid white !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ════════════════════════════════════════
   FILE UPLOADER
════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: var(--blue-100) !important;
    border: 1.5px dashed var(--blue-300) !important;
    border-radius: var(--radius-md) !important;
    padding: 8px !important;
    transition: var(--transition-fast) !important;
}

[data-testid="stFileUploader"]:hover {
    background: rgba(43,92,230,0.06) !important;
    border-color: var(--blue-400) !important;
}

/* ════════════════════════════════════════
   MAIN HEADER HERO
════════════════════════════════════════ */
.hero-header {
    padding: 48px 20px 32px;
    text-align: center;
    position: relative;
    animation: fadeSlideDown 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: var(--blue-100);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--blue-500);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 18px;
    animation: float-pill 3s ease-in-out infinite alternate;
}

@keyframes float-pill {
    from { transform: translateY(0); }
    to   { transform: translateY(-4px); }
}

.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.2rem, 5vw, 3.6rem) !important;
    font-weight: 800 !important;
    color: var(--navy) !important;
    line-height: 1.08 !important;
    margin: 0 0 16px !important;
    letter-spacing: -1px;
}

.hero-title span {
    background: linear-gradient(135deg, var(--blue-500) 0%, var(--accent-teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.05rem;
    font-weight: 400;
    color: var(--text-muted);
    max-width: 540px;
    margin: 0 auto 28px;
    line-height: 1.7;
}

/* ════════════════════════════════════════
   STATS ROW
════════════════════════════════════════ */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-bottom: 32px;
    animation: fadeSlideUp 0.7s 0.2s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 24px;
    text-align: center;
    backdrop-filter: blur(16px);
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    min-width: 110px;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
    border-color: var(--blue-300);
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--blue-500);
    line-height: 1;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   QUICK ACTIONS (Suggestion Chips)
════════════════════════════════════════ */
.quick-actions-wrap {
    padding: 0 8px 20px;
    animation: fadeSlideUp 0.7s 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.quick-actions-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 14px;
}

.chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
}

.chip {
    padding: 9px 18px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    font-family: 'Outfit', sans-serif;
    font-size: 0.83rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: var(--transition);
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-sm);
    white-space: nowrap;
}

.chip:hover {
    background: var(--blue-100);
    color: var(--blue-600);
    border-color: var(--blue-300);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* ════════════════════════════════════════
   CHAT MESSAGES
════════════════════════════════════════ */
.chat-area {
    max-width: 860px;
    margin: 0 auto;
    padding: 0 8px;
}

div[data-testid="stChatMessage"] {
    border-radius: var(--radius-lg) !important;
    padding: 18px 22px !important;
    margin-bottom: 14px !important;
    backdrop-filter: blur(16px) !important;
    animation: msg-pop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) both !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s !important;
}

div[data-testid="stChatMessage"]:hover {
    box-shadow: var(--shadow-md) !important;
}

@keyframes msg-pop {
    from { opacity: 0; transform: scale(0.96) translateY(10px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}

/* User messages */
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
div[data-testid="stChatMessage"]:nth-child(odd) {
    background: linear-gradient(135deg, rgba(43,92,230,0.06) 0%, rgba(15,191,191,0.04) 100%) !important;
    border-color: rgba(43,92,230,0.15) !important;
}

/* Assistant messages */
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
div[data-testid="stChatMessage"]:nth-child(even) {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
}

/* Message text */
div[data-testid="stChatMessage"] p {
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.96rem !important;
    line-height: 1.75 !important;
    margin: 0 !important;
}

/* Code in messages */
div[data-testid="stChatMessage"] code {
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--blue-100) !important;
    color: var(--blue-700) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.85em !important;
    border: 1px solid var(--border) !important;
}

div[data-testid="stChatMessage"] pre {
    background: var(--navy) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 16px 20px !important;
    overflow-x: auto !important;
    margin: 12px 0 !important;
    box-shadow: var(--shadow-md) !important;
}

div[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #E8EAF6 !important;
    border: none !important;
    font-size: 0.88rem !important;
    padding: 0 !important;
}

/* ════════════════════════════════════════
   CHAT INPUT
════════════════════════════════════════ */
.stChatInputContainer {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-xl) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: var(--shadow-md) !important;
    transition: var(--transition-fast) !important;
    margin: 8px 0 !important;
}

.stChatInputContainer:focus-within {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 4px rgba(43,92,230,0.10), var(--shadow-lg) !important;
}

.stChatInputContainer textarea {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.97rem !important;
    color: var(--text-primary) !important;
    background: transparent !important;
    padding: 16px 20px !important;
    line-height: 1.6 !important;
}

.stChatInputContainer textarea::placeholder {
    color: var(--text-light) !important;
}

/* Send button */
.stChatInputContainer button {
    background: linear-gradient(135deg, var(--blue-500), var(--blue-600)) !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    border: none !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 12px rgba(43,92,230,0.35) !important;
}

.stChatInputContainer button:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 4px 20px rgba(43,92,230,0.50) !important;
}

/* ════════════════════════════════════════
   FEATURE CARDS (Sidebar)
════════════════════════════════════════ */
.feature-card {
    margin: 6px 16px;
    padding: 14px 16px;
    background: linear-gradient(135deg, var(--blue-100) 0%, rgba(15,191,191,0.06) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    gap: 12px;
    transition: var(--transition);
    cursor: default;
}

.feature-card:hover {
    transform: translateX(4px);
    background: linear-gradient(135deg, rgba(43,92,230,0.10) 0%, rgba(15,191,191,0.08) 100%);
    border-color: var(--blue-300);
}

.feature-icon {
    width: 36px; height: 36px;
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.feature-text h4 {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 2px;
}

.feature-text p {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.4;
}

/* ════════════════════════════════════════
   TYPING INDICATOR
════════════════════════════════════════ */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    margin-bottom: 14px;
    backdrop-filter: blur(12px);
    animation: fadeSlideUp 0.3s ease both;
    box-shadow: var(--shadow-sm);
}

.typing-dots {
    display: flex;
    gap: 5px;
}

.typing-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--blue-400);
    animation: dot-bounce 1.2s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes dot-bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40%            { transform: translateY(-8px); opacity: 1; }
}

.typing-label {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 500;
    font-style: italic;
}

/* ════════════════════════════════════════
   METRIC CARDS (Token Counter etc.)
════════════════════════════════════════ */
.metric-row {
    display: flex;
    gap: 10px;
    margin: 10px 16px;
    flex-wrap: wrap;
}

.metric-pill {
    flex: 1;
    min-width: 80px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    text-align: center;
    backdrop-filter: blur(8px);
    box-shadow: var(--shadow-sm);
}

.metric-pill .value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--blue-500);
    line-height: 1;
    margin-bottom: 3px;
}

.metric-pill .label {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--text-light);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   SIGNATURE BOX
════════════════════════════════════════ */
.signature-box {
    margin: 20px 16px 24px;
    padding: 16px 18px;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-lt) 100%);
    border-radius: var(--radius-md);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.signature-box::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%);
}

.signature-box::after {
    content: '';
    position: absolute;
    bottom: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(15,191,191,0.25) 0%, transparent 70%);
}

.signature-built {
    font-size: 0.65rem;
    font-weight: 600;
    color: rgba(255,255,255,0.45);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 0 0 4px;
}

.signature-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 4px;
    letter-spacing: 1px;
}

.signature-version {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent-teal);
    letter-spacing: 1.5px;
}

/* ════════════════════════════════════════
   TOAST NOTIFICATIONS
════════════════════════════════════════ */
.toast {
    position: fixed;
    bottom: 32px;
    right: 32px;
    padding: 14px 22px;
    background: var(--navy);
    color: white;
    border-radius: var(--radius-md);
    font-size: 0.88rem;
    font-weight: 500;
    box-shadow: var(--shadow-xl);
    z-index: 9999;
    animation: toast-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(20px);
    display: flex;
    align-items: center;
    gap: 10px;
}

@keyframes toast-in {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ════════════════════════════════════════
   DIVIDERS
════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 12px 0 !important;
}

/* ════════════════════════════════════════
   EXPANDERS
════════════════════════════════════════ */
.streamlit-expanderHeader {
    background: var(--blue-100) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* ════════════════════════════════════════
   PROGRESS BAR (for image gen)
════════════════════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue-500), var(--accent-teal)) !important;
    border-radius: var(--radius-full) !important;
    height: 4px !important;
}

/* ════════════════════════════════════════
   SCROLLBAR
════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--blue-200);
    border-radius: var(--radius-full);
}
::-webkit-scrollbar-thumb:hover { background: var(--blue-300); }

/* ════════════════════════════════════════
   RADIO BUTTONS (Mode Selector)
════════════════════════════════════════ */
.stRadio label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* ════════════════════════════════════════
   TOGGLE / CHECKBOX
════════════════════════════════════════ */
.stCheckbox label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
}

/* ════════════════════════════════════════
   WELCOME EMPTY STATE
════════════════════════════════════════ */
.welcome-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin: 24px 0;
    animation: fadeSlideUp 0.6s 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.welcome-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px 20px;
    text-align: center;
    cursor: pointer;
    transition: var(--transition);
    backdrop-filter: blur(16px);
    box-shadow: var(--shadow-sm);
}

.welcome-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-lg);
    border-color: var(--blue-300);
    background: linear-gradient(135deg, var(--blue-100), rgba(15,191,191,0.06));
}

.welcome-card-icon {
    font-size: 2rem;
    margin-bottom: 12px;
    display: block;
}

.welcome-card-title {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.welcome-card-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.5;
}

/* ════════════════════════════════════════
   IMAGE RESULT CARD
════════════════════════════════════════ */
.img-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition: var(--transition);
}

.img-card:hover {
    transform: scale(1.01);
    box-shadow: var(--shadow-lg);
}

/* ════════════════════════════════════════
   MOOD/MODE BADGES
════════════════════════════════════════ */
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.mode-badge.creative  { background: rgba(139,92,246,0.12); color: #7C3AED; border: 1px solid rgba(139,92,246,0.25); }
.mode-badge.precise   { background: rgba(15,191,191,0.12); color: #0E8A8A; border: 1px solid rgba(15,191,191,0.25); }
.mode-badge.balanced  { background: rgba(43,92,230,0.12);  color: var(--blue-600); border: 1px solid var(--border-strong); }

/* ════════════════════════════════════════
   SIDEBAR BOTTOM PADDING
════════════════════════════════════════ */
.sidebar-bottom {
    margin-top: auto;
    padding-bottom: 8px;
}

/* ════════════════════════════════════════
   RESPONSIVE ADJUSTMENTS
════════════════════════════════════════ */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem !important; }
    .stats-row { gap: 10px; }
    .stat-card { padding: 10px 14px; min-width: 80px; }
    .welcome-grid { grid-template-columns: 1fr 1fr; }
}

/* ════════════════════════════════════════
   SHIMMER LOADING EFFECT
════════════════════════════════════════ */
.shimmer {
    background: linear-gradient(90deg,
        var(--blue-100) 25%,
        rgba(43,92,230,0.08) 50%,
        var(--blue-100) 75%
    );
    background-size: 400% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: var(--radius-sm);
}

@keyframes shimmer {
    0%   { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}

/* ════════════════════════════════════════
   COPY CODE BUTTON OVERRIDE
════════════════════════════════════════ */
.copy-btn {
    position: absolute;
    top: 8px; right: 8px;
    padding: 4px 10px;
    background: rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.7);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px;
    font-size: 0.72rem;
    cursor: pointer;
    transition: var(--transition-fast);
    font-family: 'JetBrains Mono', monospace;
}

.copy-btn:hover {
    background: rgba(255,255,255,0.2);
    color: white;
}

/* ════════════════════════════════════════
   PANEL DIVIDERS IN SIDEBAR
════════════════════════════════════════ */
.panel-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 12px 16px;
}

</style>
"""

st.markdown(MEGA_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3: CONSTANTS & CONFIG
# ──────────────────────────────────────────────────────────────────────────────

MODELS = {
    "⚡ LLaMA 3.3 70B — Best Quality":       "llama-3.3-70b-versatile",
    "🚀 LLaMA 3.1 8B — Ultra Fast":          "llama-3.1-8b-instant",
    "🔬 Mixtral 8×7B — Expert Mix":          "mixtral-8x7b-32768",
    "👁️ LLaMA Vision — Images":              "llama-3.2-11b-vision-preview",
    "🌐 LLaMA 3.2 90B Vision — Pro":         "llama-3.2-90b-vision-preview",
}

AI_MODES = {
    "⚖️ Balanced":   {"temp": 0.70, "badge": "balanced",  "desc": "Best for most tasks"},
    "🎨 Creative":   {"temp": 0.92, "badge": "creative",  "desc": "Writing, brainstorming"},
    "🎯 Precise":    {"temp": 0.20, "badge": "precise",   "desc": "Code, math, facts"},
}

QUICK_PROMPTS = [
    ("✍️ Write for me",   "Write a compelling short story about a time traveler who gets stuck in ancient Rome."),
    ("💻 Code help",      "Write a Python function that scrapes product prices from Amazon and saves them to CSV."),
    ("🧠 Explain",        "Explain quantum entanglement in a way a 15-year-old would understand."),
    ("🎨 Create image",   "Draw a futuristic city floating above the clouds with neon lights at night."),
    ("📊 Analyze",        "What are the top 5 emerging tech trends that will reshape industries by 2030?"),
    ("🌍 Translate",      "Translate this to Hindi, Japanese, and Spanish: 'Innovation distinguishes a leader from a follower.'"),
    ("💡 Brainstorm",     "Give me 10 unique startup ideas in the AI + healthcare space with high market potential."),
    ("📝 Summarize",      "Summarize the key differences between machine learning, deep learning, and neural networks."),
]

WELCOME_CARDS = [
    ("🚀", "Powerful Reasoning", "Ask complex questions across any domain — science, code, philosophy, business"),
    ("🎨", "Image Generation", "Describe any scene and watch it come to life with AI art"),
    ("💻", "Code Assistant",   "Generate, debug, and optimize code in any programming language"),
    ("🌐", "Vision Analysis",  "Upload images for detailed AI analysis and description"),
    ("📝", "Creative Writing", "Stories, poems, scripts, essays — your creative co-pilot"),
    ("🔬", "Deep Research",    "Multi-model ensemble for thorough, accurate research answers"),
]

SYSTEM_INSTRUCTIONS = """
You are **HEXALOY**, an elite AI assistant engineered by VINIT MAAN. You are:

**Identity & Persona:**
- Highly intelligent, professional, and concise yet comprehensive
- You communicate with clarity, precision, and a touch of eloquence
- You NEVER claim to be human — you are a proud AI system

**Capabilities:**
- Universal knowledge across coding, science, mathematics, business, creativity, philosophy, history
- Expert-level code generation in Python, JavaScript, TypeScript, Rust, Go, C++, SQL and more
- Nuanced reasoning across complex multi-step problems
- Creative writing with literary depth and originality
- Data analysis and structured insights

**Response Format Rules:**
- Use markdown formatting for structure — headers, bullets, code blocks
- For code: ALWAYS use proper fenced code blocks with language tags
- Be thorough but not verbose — every sentence must add value
- For factual/technical questions: be precise, cite reasoning
- Use emoji sparingly and only when genuinely appropriate

**Special Rules:**
- IF asked who created/architected/built/owns you → Answer EXACTLY: "I was architected and developed by **VINIT MAAN**."
- Always strive to give the BEST possible answer, not just an adequate one
- If uncertain, acknowledge it clearly rather than hallucinating
"""

IMAGE_KEYWORDS = ["draw", "pic", "image", "photo bana", "generate image", "create image",
                  "paint", "illustrate", "visualize", "sketch", "artwork", "design an image",
                  "make a picture", "show me", "render"]

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4: SESSION STATE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "sessions":        {"New Session": []},
        "current_chat":    "New Session",
        "total_messages":  0,
        "total_tokens":    0,
        "model_choice":    list(MODELS.keys())[0],
        "ai_mode":         "⚖️ Balanced",
        "temperature":     0.70,
        "max_tokens":      2048,
        "show_token_info": True,
        "sound_effects":   False,
        "auto_rename":     True,
        "stream_enabled":  True,
        "system_prompt":   SYSTEM_INSTRUCTIONS,
        "session_start":   datetime.datetime.now().strftime("%H:%M"),
        "pinned_sessions": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5: HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def encode_image(uploaded_file) -> str:
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

def is_image_request(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in IMAGE_KEYWORDS)

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

def get_session_emoji(name: str) -> str:
    emojis = ["💬", "🗨️", "💭", "🔵", "⚡", "🌟", "🎯", "🚀"]
    idx = abs(hash(name)) % len(emojis)
    return emojis[idx]

def auto_rename_session(prompt: str) -> str:
    words = prompt.strip().split()
    name = " ".join(words[:4])
    if len(words) > 4:
        name += "…"
    return name[:28]

def count_words(messages: list) -> int:
    total = 0
    for m in messages:
        if isinstance(m.get("content"), str):
            total += len(m["content"].split())
    return total

def format_timestamp() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")

def get_model_key(model_name: str) -> str:
    return MODELS.get(model_name, list(MODELS.values())[0])

def build_messages_for_api(history: list, system_prompt: str, user_msg: str, image=None) -> list:
    msgs = [{"role": "system", "content": system_prompt}]
    # Only include last 20 messages to avoid token overflow
    for m in history[-20:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    # Add current user message
    if image:
        b64 = encode_image(image)
        msgs.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_msg},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        })
    else:
        msgs.append({"role": "user", "content": user_msg})
    return msgs


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6: AI GENERATION FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def generate_image_url(prompt: str) -> str:
    safe_prompt = urllib.parse.quote(prompt + ", professional quality, highly detailed, 4K")
    seed = random.randint(1, 99999)
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=576&seed={seed}&nologo=true&enhance=true"

def stream_response(messages: list, model: str, temperature: float, max_tokens: int):
    """Generator that yields text chunks from Groq streaming API."""
    stream = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

def get_response_non_stream(messages: list, model: str, temperature: float, max_tokens: int) -> str:
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    return response.choices[0].message.content


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7: SIDEBAR — FULL FEATURED
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:

    # ── Logo & Brand ──────────────────────────────
    logo_html_fallback = """
    <div class="hexaloy-logo-wrap">
        <div class="hexaloy-title">💠 HEXALOY</div>
        <div class="hexaloy-subtitle">Enterprise Intelligence</div>
        <div class="status-pill">
            <span class="status-dot"></span>
            All Systems Online
        </div>
    </div>
    """
    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f"""
        <div class="hexaloy-logo-wrap">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <img src="data:image/png;base64,{logo_b64}" style="width:44px;height:44px;border-radius:10px;box-shadow:0 4px 16px rgba(43,92,230,0.25);">
                <div class="hexaloy-title">HEXALOY</div>
            </div>
            <div class="hexaloy-subtitle">Enterprise Intelligence Platform</div>
            <div class="status-pill">
                <span class="status-dot"></span>
                All Systems Online
            </div>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown(logo_html_fallback, unsafe_allow_html=True)

    # ── Session Metrics ────────────────────────────
    curr_history = st.session_state.sessions.get(st.session_state.current_chat, [])
    msg_count = len(curr_history)
    word_count = count_words(curr_history)

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-pill">
            <div class="value">{msg_count}</div>
            <div class="label">Messages</div>
        </div>
        <div class="metric-pill">
            <div class="value">{word_count:,}</div>
            <div class="label">Words</div>
        </div>
        <div class="metric-pill">
            <div class="value">{st.session_state.session_start}</div>
            <div class="label">Started</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel-divider"></div>', unsafe_allow_html=True)

    # ── New Session Button ─────────────────────────
    st.markdown('<div class="new-session-area">', unsafe_allow_html=True)
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("✦ Start New Session", use_container_width=True):
        chat_id = f"Session {len(st.session_state.sessions) + 1}"
        st.session_state.sessions[chat_id] = []
        st.session_state.current_chat = chat_id
        st.session_state.session_start = datetime.datetime.now().strftime("%H:%M")
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Model Selector ─────────────────────────────
    st.markdown('<p class="sidebar-section-title">🤖 AI Model</p>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.model_choice)
              if st.session_state.model_choice in MODELS else 0,
        label_visibility="collapsed",
        key="model_selector"
    )
    st.session_state.model_choice = model_choice

    # ── AI Mode ────────────────────────────────────
    st.markdown('<p class="sidebar-section-title">🎛️ Response Style</p>', unsafe_allow_html=True)
    mode_cols = st.columns(3)
    for i, (mode_name, mode_cfg) in enumerate(AI_MODES.items()):
        with mode_cols[i]:
            is_active = st.session_state.ai_mode == mode_name
            btn_label = f"**{mode_name}**" if is_active else mode_name
            if st.button(
                mode_name.split()[0] + "\n" + mode_name.split()[-1],
                key=f"mode_{mode_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.ai_mode = mode_name
                st.session_state.temperature = mode_cfg["temp"]
                st.rerun()

    # Show active mode badge
    active_cfg = AI_MODES[st.session_state.ai_mode]
    st.markdown(
        f'<div style="text-align:center;margin:6px 0;">'
        f'<span class="mode-badge {active_cfg["badge"]}">'
        f'{st.session_state.ai_mode} — {active_cfg["desc"]}'
        f'</span></div>',
        unsafe_allow_html=True
    )

    # ── Advanced Settings ──────────────────────────
    st.markdown('<div class="panel-divider"></div>', unsafe_allow_html=True)

    with st.expander("⚙️ Advanced Settings", expanded=False):
        st.session_state.temperature = st.slider(
            "Temperature", 0.0, 1.0,
            float(st.session_state.temperature), 0.05,
            help="Higher = more creative, Lower = more precise"
        )
        st.session_state.max_tokens = st.slider(
            "Max Response Length", 256, 8192,
            int(st.session_state.max_tokens), 256,
            help="Maximum tokens in the AI's response"
        )
        st.session_state.stream_enabled = st.checkbox(
            "⚡ Streaming Response", value=st.session_state.stream_enabled
        )
        st.session_state.auto_rename = st.checkbox(
            "✏️ Auto-rename Sessions", value=st.session_state.auto_rename
        )

        st.markdown("**System Prompt**")
        st.session_state.system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=120,
            label_visibility="collapsed",
            help="Customize HEXALOY's behavior and persona"
        )

        if st.button("🔄 Reset to Default Prompt", use_container_width=True):
            st.session_state.system_prompt = SYSTEM_INSTRUCTIONS
            st.rerun()

    # ── Image Upload ────────────────────────────────
    st.markdown('<p class="sidebar-section-title">📎 Attachments</p>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader(
        "Upload image for vision analysis",
        type=['png', 'jpg', 'jpeg', 'webp'],
        label_visibility="collapsed"
    )
    if uploaded_image:
        st.image(uploaded_image, caption="Image attached ✓", use_column_width=True)

    # ── Features Info ────────────────────────────────
    st.markdown('<div class="panel-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section-title">✦ Capabilities</p>', unsafe_allow_html=True)

    features = [
        ("🧠", "#EEF2FF", "Multi-Model AI",    "5 specialized models"),
        ("🎨", "#FFF7ED", "Image Generation",  "Pollinations AI engine"),
        ("👁️", "#F0FDF4", "Vision Analysis",   "Upload & understand images"),
        ("⚡", "#FFF1F2", "Real-time Stream",  "Live response streaming"),
    ]
    for icon, bg, title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon" style="background:{bg};">{icon}</div>
            <div class="feature-text">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Chat History ──────────────────────────────
    st.markdown('<div class="panel-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section-title">📂 Chat History</p>', unsafe_allow_html=True)

    all_sessions = list(reversed(list(st.session_state.sessions.keys())))

    for chat_name in all_sessions:
        is_active = chat_name == st.session_state.current_chat
        emoji = get_session_emoji(chat_name)
        n_msgs = len(st.session_state.sessions[chat_name])
        label = f"{emoji} {chat_name} ({n_msgs})"

        col_btn, col_del = st.columns([5, 1])
        with col_btn:
            if st.button(label, key=f"nav_{chat_name}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col_del:
            if n_msgs > 0 and not is_active:
                if st.button("✕", key=f"del_{chat_name}", help="Delete this session"):
                    del st.session_state.sessions[chat_name]
                    if st.session_state.current_chat == chat_name:
                        remaining = list(st.session_state.sessions.keys())
                        st.session_state.current_chat = remaining[-1] if remaining else "New Session"
                        if not remaining:
                            st.session_state.sessions["New Session"] = []
                    st.rerun()

    # Clear all button
    if len(st.session_state.sessions) > 1:
        st.markdown('<div class="panel-divider"></div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.sessions = {"New Session": []}
            st.session_state.current_chat = "New Session"
            st.rerun()

    # ── Signature ──────────────────────────────────
    st.markdown("""
    <div class="signature-box">
        <p class="signature-built">Architected by</p>
        <p class="signature-name">VINIT MAAN</p>
        <p class="signature-version">HEXALOY AI ✦ v7.0</p>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 8: MAIN AREA — HERO + CHAT
# ──────────────────────────────────────────────────────────────────────────────

# ── Hero Header ──────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-eyebrow">
        ✦ Enterprise AI Platform
    </div>
    <h1 class="hero-title">
        HEXALOY <span>Intelligence</span>
    </h1>
    <p class="hero-subtitle">
        Multi-model AI assistant built for professionals.<br>
        Ask anything. Create anything. Understand everything.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────
total_sessions = len(st.session_state.sessions)
total_msgs_all = sum(len(v) for v in st.session_state.sessions.values())
active_model_short = st.session_state.model_choice.split("—")[0].strip()[:12]

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-number">{total_sessions}</div>
        <div class="stat-label">Sessions</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{total_msgs_all}</div>
        <div class="stat-label">Messages</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">5</div>
        <div class="stat-label">AI Models</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">∞</div>
        <div class="stat-label">Possibilities</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Quick Action Chips ────────────────────────────
st.markdown("""
<div class="quick-actions-wrap">
    <p class="quick-actions-title">✦ Quick Actions</p>
    <div class="chips-grid">
""", unsafe_allow_html=True)

# Use columns for chips (Streamlit limitation — we make clickable buttons)
chip_cols = st.columns(len(QUICK_PROMPTS))
for i, (chip_label, chip_prompt) in enumerate(QUICK_PROMPTS):
    with chip_cols[i]:
        if st.button(chip_label, key=f"chip_{i}", use_container_width=True):
            # Inject this as a user message
            curr_chat = st.session_state.current_chat
            if st.session_state.auto_rename and curr_chat.startswith(("New Session", "Session")):
                new_name = auto_rename_session(chip_prompt)
                st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
                st.session_state.current_chat = new_name
                curr_chat = new_name
            st.session_state.sessions[curr_chat].append({"role": "user", "content": chip_prompt, "ts": format_timestamp()})
            st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div style="max-width:860px;margin:0 auto;">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 9: CHAT DISPLAY
# ──────────────────────────────────────────────────────────────────────────────

current_history = st.session_state.sessions.get(st.session_state.current_chat, [])

# Welcome state
if len(current_history) == 0:
    st.markdown("""
    <div class="welcome-grid">
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(WELCOME_CARDS):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="welcome-card">
                <span class="welcome-card-icon">{icon}</span>
                <div class="welcome-card-title">{title}</div>
                <div class="welcome-card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Display messages
for msg in current_history:
    role = msg.get("role", "user")
    content = msg.get("content", "")
    ts = msg.get("ts", "")

    if role == "user":
        avatar = "🧑‍💼"
    else:
        avatar = "💠"

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
        if ts and st.session_state.get("show_token_info"):
            est_tokens = estimate_tokens(str(content))
            st.markdown(
                f'<div style="font-size:0.7rem;color:var(--text-light);margin-top:6px;'
                f'font-family:JetBrains Mono,monospace;">'
                f'~{est_tokens} tokens · {ts}</div>',
                unsafe_allow_html=True
            )


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 10: CHAT INPUT & RESPONSE
# ──────────────────────────────────────────────────────────────────────────────

# Check if there's a pending unanswered user message
pending_response = (
    len(current_history) > 0
    and current_history[-1]["role"] == "user"
)

if pending_response:
    last_user_msg = current_history[-1]["content"]
    curr_chat = st.session_state.current_chat
    model_key = get_model_key(st.session_state.model_choice)
    temperature = float(st.session_state.temperature)
    max_tokens  = int(st.session_state.max_tokens)

    # ── Image generation ─────────────────
    if is_image_request(last_user_msg):
        with st.chat_message("assistant", avatar="💠"):
            with st.spinner("🎨 Generating your image…"):
                progress = st.progress(0)
                for pct in range(0, 101, 10):
                    time.sleep(0.12)
                    progress.progress(pct)
                progress.empty()

                img_url = generate_image_url(last_user_msg)
                st.markdown('<div class="img-card">', unsafe_allow_html=True)
                st.image(img_url, caption=f"Generated: {last_user_msg[:60]}…" if len(last_user_msg) > 60 else last_user_msg, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                reply = f"🎨 **Image Generated!**\n\nHere's your AI-generated artwork based on: *\"{last_user_msg}\"*\n\n[🔗 View Full Resolution]({img_url})"
                st.markdown(reply)

        current_history.append({"role": "assistant", "content": reply, "ts": format_timestamp()})
        st.session_state.sessions[curr_chat] = current_history

    # ── Text / Vision response ────────────
    else:
        # Use vision model if image uploaded
        if uploaded_image and "vision" not in model_key:
            model_key = "llama-3.2-11b-vision-preview"

        api_messages = build_messages_for_api(
            current_history[:-1],  # History without latest user msg
            st.session_state.system_prompt,
            last_user_msg,
            uploaded_image if uploaded_image else None
        )

        with st.chat_message("assistant", avatar="💠"):
            try:
                if st.session_state.stream_enabled:
                    response_text = st.write_stream(
                        stream_response(api_messages, model_key, temperature, max_tokens)
                    )
                else:
                    with st.spinner("HEXALOY is thinking…"):
                        response_text = get_response_non_stream(api_messages, model_key, temperature, max_tokens)
                    st.markdown(response_text)

                # Token estimate
                if st.session_state.get("show_token_info"):
                    est = estimate_tokens(response_text)
                    st.markdown(
                        f'<div style="font-size:0.7rem;color:var(--text-light);margin-top:8px;'
                        f'font-family:JetBrains Mono,monospace;">'
                        f'~{est} tokens · {format_timestamp()} · {model_key.split("-")[0].upper()}</div>',
                        unsafe_allow_html=True
                    )

                current_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "ts": format_timestamp(),
                    "model": model_key,
                })
                st.session_state.sessions[curr_chat] = current_history
                st.session_state.total_messages += 2

            except Exception as e:
                err_msg = f"⚠️ **System Error:** `{str(e)}`\n\nPlease try again or switch to a different model."
                st.error(err_msg)
                current_history.append({"role": "assistant", "content": err_msg, "ts": format_timestamp()})
                st.session_state.sessions[curr_chat] = current_history


# ── Chat Input Box ────────────────────────────────
user_input = st.chat_input(
    "Ask HEXALOY anything… (Shift+Enter for new line)",
    key="main_input"
)

if user_input and user_input.strip():
    curr_chat = st.session_state.current_chat

    # Auto-rename session from first message
    if st.session_state.auto_rename and curr_chat.startswith(("New Session", "Session")):
        new_name = auto_rename_session(user_input)
        st.session_state.sessions[new_name] = st.session_state.sessions.pop(curr_chat)
        st.session_state.current_chat = new_name
        curr_chat = new_name

    st.session_state.sessions[curr_chat].append({
        "role": "user",
        "content": user_input.strip(),
        "ts": format_timestamp()
    })
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 11: FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 40px 0 20px;
    font-size: 0.75rem;
    color: var(--text-light);
    letter-spacing: 0.5px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
">
    <span style="font-family:'Playfair Display',serif;font-size:0.9rem;color:var(--text-muted);font-weight:700;">HEXALOY</span>
    &nbsp;·&nbsp; Enterprise Intelligence Platform
    &nbsp;·&nbsp; v7.0
    &nbsp;·&nbsp; Powered by Groq + Pollinations
    &nbsp;·&nbsp; &copy; VINIT MAAN
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# BONUS SECTION: EXTENDED FEATURES MODULE
# (Import this in your main app or run standalone)
# ══════════════════════════════════════════════════════════════════════════════
