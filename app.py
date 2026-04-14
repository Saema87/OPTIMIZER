import streamlit as st
from openai import OpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Prompt Optimizer",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FORCE LIGHT THEME + GLASSMORPHISM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════
   FORCE LIGHT THEME ON ALL STREAMLIT INTERNALS
   ═══════════════════════════════════════ */

/* Root overrides — kill all dark colors */
:root,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp,
.main,
.block-container,
section[data-testid="stSidebar"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    background-color: #f0f4ff !important;
    color: #1f2937 !important;
}

/* App background */
.stApp {
    background: #f0f4ff !important;
    font-family: 'Outfit', sans-serif !important;
    position: relative;
    overflow-x: hidden;
}

/* Main container */
[data-testid="stAppViewContainer"] > section > div {
    background-color: transparent !important;
}

/* Gradient mesh overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 600px 500px at 15% 20%, rgba(168, 130, 255, 0.25), transparent),
        radial-gradient(ellipse 500px 600px at 85% 15%, rgba(99, 200, 255, 0.22), transparent),
        radial-gradient(ellipse 700px 400px at 50% 80%, rgba(255, 170, 200, 0.18), transparent),
        radial-gradient(ellipse 400px 400px at 75% 60%, rgba(160, 255, 200, 0.15), transparent);
    pointer-events: none;
    z-index: 0;
}

/* Animated blobs */
.blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.4;
    pointer-events: none;
    z-index: 0;
    animation: blobFloat 20s ease-in-out infinite;
}
.blob-1 {
    width: 350px; height: 350px;
    background: linear-gradient(135deg, #c084fc, #818cf8);
    top: -80px; left: -60px;
    animation-delay: 0s;
}
.blob-2 {
    width: 280px; height: 280px;
    background: linear-gradient(135deg, #67e8f9, #6ee7b7);
    top: 30%; right: -80px;
    animation-delay: -7s;
}
.blob-3 {
    width: 320px; height: 320px;
    background: linear-gradient(135deg, #fda4af, #fdba74);
    bottom: -60px; left: 20%;
    animation-delay: -14s;
}
@keyframes blobFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(30px, -40px) scale(1.05); }
    50% { transform: translate(-20px, 20px) scale(0.95); }
    75% { transform: translate(15px, 35px) scale(1.03); }
}

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

.block-container {
    padding-top: 2rem !important;
    max-width: 740px !important;
    position: relative;
    z-index: 1;
    background: transparent !important;
}

/* ═══════════════════════════════════════
   HERO
   ═══════════════════════════════════════ */
.hero-wrap { text-align: center; padding: 12px 0 28px; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.8); border-radius: 100px;
    padding: 8px 22px; font-size: 11px; letter-spacing: 2.5px;
    text-transform: uppercase; color: #7c3aed;
    font-family: 'JetBrains Mono', monospace; font-weight: 500;
    box-shadow: 0 2px 12px rgba(124,58,237,0.08);
}
.hero-title {
    font-size: clamp(30px, 5.5vw, 48px); font-weight: 800; line-height: 1.08;
    background: linear-gradient(135deg, #1e1b4b 0%, #7c3aed 50%, #2563eb 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 20px 0 10px; letter-spacing: -0.5px;
}
.hero-sub { color: #6b7280; font-size: 16px; font-weight: 400; }

/* ═══════════════════════════════════════
   RESULT CARD
   ═══════════════════════════════════════ */
.result-card {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px);
    border: 1px solid rgba(124, 58, 237, 0.15); border-radius: 20px;
    padding: 28px; margin-top: 8px;
    box-shadow: 0 12px 40px rgba(124,58,237,0.08), inset 0 1px 0 rgba(255,255,255,0.9);
    animation: slideUp 0.5s ease-out;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
.result-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px; flex-wrap: wrap;
}
.result-label {
    font-size: 10.5px; text-transform: uppercase; letter-spacing: 2px;
    color: #9ca3af; font-family: 'JetBrains Mono', monospace; font-weight: 500;
}
.tag {
    padding: 4px 14px; border-radius: 100px;
    font-size: 11px; font-weight: 600; font-family: 'Outfit', sans-serif;
}
.tag-tool { background: rgba(124,58,237,0.1); color: #7c3aed; border: 1px solid rgba(124,58,237,0.15); }
.tag-media { background: rgba(59,130,246,0.08); color: #3b82f6; border: 1px solid rgba(59,130,246,0.12); text-transform: capitalize; }
.tag-tone { background: rgba(16,185,129,0.08); color: #059669; border: 1px solid rgba(16,185,129,0.12); }
.result-box {
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.6); border-radius: 14px;
    padding: 22px; font-size: 14.5px; line-height: 1.8;
    color: #374151 !important; white-space: pre-wrap; word-break: break-word;
    font-family: 'Outfit', sans-serif; max-height: 420px; overflow-y: auto;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.03);
}
.result-meta {
    display: flex; justify-content: space-between;
    margin-top: 12px; font-size: 11px; color: #9ca3af;
    font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════
   FORCE LIGHT ON ALL STREAMLIT WIDGETS
   ═══════════════════════════════════════ */

/* Text Input */
.stTextInput > label {
    color: #6b7280 !important; font-size: 10.5px !important;
    text-transform: uppercase !important; letter-spacing: 2px !important;
    font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important;
}
.stTextInput > div > div > input,
.stTextInput > div > div {
    background: rgba(255,255,255,0.5) !important;
    background-color: rgba(255,255,255,0.5) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    border-radius: 14px !important;
    color: #1f2937 !important;
    font-size: 16px !important; padding: 15px 18px !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.8) !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(124,58,237,0.4) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1), 0 4px 20px rgba(124,58,237,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #b0b8c8 !important; }

/* Radio & Select labels */
.stRadio > label, .stSelectbox > label {
    color: #6b7280 !important; font-size: 10.5px !important;
    text-transform: uppercase !important; letter-spacing: 2px !important;
    font-family: 'JetBrains Mono', monospace !important; font-weight: 500 !important;
}

/* Radio buttons */
div[role="radiogroup"] { gap: 8px !important; flex-wrap: wrap !important; }
div[role="radiogroup"] label {
    background: rgba(255,255,255,0.45) !important;
    background-color: rgba(255,255,255,0.45) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    border-radius: 12px !important; padding: 10px 20px !important;
    color: #6b7280 !important; font-size: 13px !important; font-weight: 500 !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}
div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(124,58,237,0.1) !important;
    background-color: rgba(124,58,237,0.1) !important;
    border-color: rgba(124,58,237,0.35) !important;
    color: #7c3aed !important; font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.1) !important;
}
/* Radio dot color */
div[role="radiogroup"] label span[data-checked="true"],
div[role="radiogroup"] input:checked + div {
    color: #7c3aed !important;
    border-color: #7c3aed !important;
}

/* Select box */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.5) !important;
    background-color: rgba(255,255,255,0.5) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    border-radius: 14px !important; color: #374151 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
}
/* Select dropdown */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[role="listbox"] {
    background: rgba(255,255,255,0.95) !important;
    background-color: rgba(255,255,255,0.95) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
}
[data-baseweb="menu"] li,
ul[role="listbox"] li {
    color: #374151 !important;
    background: transparent !important;
}
[data-baseweb="menu"] li:hover,
ul[role="listbox"] li:hover {
    background: rgba(124,58,237,0.08) !important;
    color: #7c3aed !important;
}

/* Button */
.stButton > button {
    width: 100% !important; padding: 16px 24px !important;
    border-radius: 16px !important; border: none !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 50%, #3b82f6 100%) !important;
    color: #fff !important; font-size: 15px !important; font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important; letter-spacing: 0.3px !important;
    box-shadow: 0 8px 28px rgba(124,58,237,0.25), 0 2px 8px rgba(124,58,237,0.15) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 36px rgba(124,58,237,0.3), 0 4px 12px rgba(124,58,237,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button p { color: #fff !important; }

/* Code block (copy area) — force light */
.stCodeBlock,
[data-testid="stCode"],
pre, code {
    background: rgba(255,255,255,0.5) !important;
    background-color: rgba(255,255,255,0.5) !important;
    color: #374151 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
}
/* Code copy button */
[data-testid="stCode"] button,
.stCodeBlock button {
    background: rgba(255,255,255,0.7) !important;
    color: #6b7280 !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
}

/* Spinner */
.stSpinner > div { color: #7c3aed !important; }

/* Alert/Warning/Error boxes */
[data-testid="stAlert"],
.stAlert {
    background: rgba(255,255,255,0.7) !important;
    background-color: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 14px !important;
    color: #374151 !important;
}

/* Divider */
hr { border-color: rgba(124,58,237,0.08) !important; margin: 20px 0 !important; }

/* Tooltip & popover */
[data-testid="stTooltipContent"] {
    background: rgba(255,255,255,0.95) !important;
    color: #374151 !important;
}

/* Footer */
.footer {
    text-align: center; color: #b0b8c8; font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 48px; padding-bottom: 24px; letter-spacing: 0.5px;
}

/* Scrollbar */
.result-box::-webkit-scrollbar { width: 6px; }
.result-box::-webkit-scrollbar-track { background: transparent; }
.result-box::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.15); border-radius: 3px; }

/* ═══════════════════════════════════════
   NUKE ANY REMAINING DARK BACKGROUNDS
   ═══════════════════════════════════════ */
[data-testid="stBottomBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
.stMarkdown,
.element-container {
    background: transparent !important;
    background-color: transparent !important;
    color: #1f2937 !important;
}

/* Target iframe/embed containers */
iframe { background: transparent !important; }

</style>

<!-- Floating blobs -->
<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="blob blob-3"></div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS_LIST = ["ChatGPT", "Claude", "Gemini", "Grok"]
MEDIA_DISPLAY = ["✎ Text", "◻ Image", "♫ Audio", "▶ Video"]
MEDIA_MAP = {"✎ Text": "Text", "◻ Image": "Image", "♫ Audio": "Audio", "▶ Video": "Video"}
TONES = ["Professional", "Creative", "Casual", "Academic", "Persuasive", "Technical"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SYSTEM PROMPT BUILDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def build_system_prompt(media_type, tool, tone):
    tool_hints = {
        "ChatGPT": "Optimize for OpenAI ChatGPT / DALL-E. Use ChatGPT-style prompt patterns. For images, use DALL-E prompt best practices (detailed scene description, style keywords, lighting, composition). For text, leverage system-level instructions and structured output hints.",
        "Claude": "Optimize for Anthropic Claude. Use Claude-style prompt patterns with XML tags where helpful, clear task decomposition, and explicit constraints.",
        "Gemini": "Optimize for Google Gemini. Use Gemini-style prompting with clear instructions, examples where useful, and structured formatting. For images, use Imagen-compatible prompt patterns.",
        "Grok": "Optimize for xAI Grok / Aurora. Use direct, clear instructions. For images, use Aurora image generation prompt patterns with vivid descriptive language, art style references, and composition details.",
    }
    media_hints = {
        "Text": "Generate a detailed text generation super-prompt. Include: role/persona, context, specific task, format requirements, constraints, tone guidance, and example structure if helpful.",
        "Image": "Generate a detailed image generation super-prompt. Include: subject, scene composition, art style, lighting, color palette, mood/atmosphere, camera angle, level of detail, negative prompt suggestions, and technical parameters (aspect ratio, quality).",
        "Audio": "Generate a detailed audio generation super-prompt. Include: genre, mood, tempo/BPM, instruments, vocal style, duration, structure (intro/verse/chorus), production quality descriptors, and reference style.",
        "Video": "Generate a detailed video generation super-prompt. Include: scene description, camera movement, duration, visual style, transitions, pacing, color grading, subject action/motion, and cinematic references.",
    }
    return f"""You are a world-class prompt engineer. Your job is to take a short, vague, or single-word input and transform it into a highly detailed, optimized super-prompt.

{tool_hints.get(tool, tool_hints["ChatGPT"])}

{media_hints.get(media_type, media_hints["Text"])}

Tone: {tone}

RULES:
- Output ONLY the expanded super-prompt text, nothing else
- No preamble, no explanation, no markdown formatting
- Make it immediately copy-pasteable
- Be specific, vivid, and actionable
- Include all relevant parameters and details for the chosen media type
- The prompt should be 150-400 words depending on complexity
- If the input is just one word or very short, infer the most impressive and useful interpretation"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROQ CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="hero-wrap">
    <span class="hero-badge">✨ prompt optimizer</span>
    <div class="hero-title">One Word In.<br>Super Prompt Out.</div>
    <p class="hero-sub">Transform any short idea into a detailed, tool‑optimized prompt</p>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT CONTROLS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
user_input = st.text_input(
    "💡 your idea",
    placeholder="Type anything… sunset, dragon, coffee shop, AI tutor…",
)

col1, col2 = st.columns(2)
with col1:
    media_choice = st.radio("📦 output type", MEDIA_DISPLAY, horizontal=True)
with col2:
    tone = st.selectbox("🎭 tone", TONES)

tool = st.radio("🤖 optimize for", TOOLS_LIST, horizontal=True)

media_type = MEDIA_MAP[media_choice]

generate = st.button(
    f"⚡  Generate {media_type} Prompt → {tool}",
    use_container_width=True,
    type="primary",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GENERATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if generate:
    if not user_input.strip():
        st.warning("Please enter a word or short idea first.")
    else:
        client = get_client()
        if client is None:
            st.error("⚠️ GROQ_API_KEY not found. Add it in Settings → Secrets.")
        else:
            with st.spinner("✨ Crafting your super prompt…"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": build_system_prompt(media_type, tool, tone)},
                            {"role": "user", "content": f'Expand this into a detailed super-prompt: "{user_input.strip()}"'},
                        ],
                        max_tokens=1024,
                        temperature=0.8,
                    )
                    result = response.choices[0].message.content
                    st.session_state["last_result"] = result
                    st.session_state["last_meta"] = {
                        "tool": tool,
                        "media": media_type,
                        "tone": tone,
                        "words": len(result.split()),
                        "chars": len(result),
                        "input": user_input.strip(),
                    }
                except Exception as e:
                    st.error(f"❌ {str(e)}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "last_result" in st.session_state:
    r = st.session_state["last_result"]
    m = st.session_state["last_meta"]

    st.markdown("---")
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <span class="result-label">optimized prompt</span>
            <span class="tag tag-tool">{m["tool"]}</span>
            <span class="tag tag-media">{m["media"]}</span>
            <span class="tag tag-tone">{m["tone"]}</span>
        </div>
        <div class="result-box">{r}</div>
        <div class="result-meta">
            <span>{m["words"]} words · {m["chars"]} chars · "{m["input"]}"</span>
            <span>llama 3.3 70b via groq</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Code block with built-in copy button
    st.code(r, language=None)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="footer">
    free forever · groq api + streamlit cloud · no sign‑up · no gpu
</div>
""", unsafe_allow_html=True)
