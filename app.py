import streamlit as st
from openai import OpenAI
import time

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
# CUSTOM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* Global */
.stApp {
    background: #0a0a0b;
    color: #e4e4e7;
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 720px;}

/* Header */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 8px 20px;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #71717a;
    font-family: 'Space Mono', monospace;
}
.hero-title {
    font-size: clamp(28px, 5vw, 42px);
    font-weight: 700;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 16px 0 8px;
}
.hero-sub {
    color: #71717a;
    font-size: 15px;
    margin-bottom: 24px;
}

/* Section cards */
.section-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}
.section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #52525b;
    font-family: 'Space Mono', monospace;
    margin-bottom: 12px;
}

/* Result box */
.result-box {
    background: rgba(0,0,0,0.4);
    border-radius: 12px;
    padding: 20px;
    font-size: 14px;
    line-height: 1.75;
    color: #d4d4d8;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Sans', sans-serif;
    max-height: 420px;
    overflow-y: auto;
    border: 1px solid rgba(255,255,255,0.06);
}
.result-meta {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 11px;
    color: #3f3f46;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}
.tag {
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
}
.tag-tool {
    background: rgba(139,92,246,0.15);
    color: #a78bfa;
}
.tag-media {
    background: rgba(255,255,255,0.06);
    color: #71717a;
    text-transform: capitalize;
}

/* Fix Streamlit widget styling */
.stTextInput > div > div > input {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-size: 16px !important;
    padding: 14px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 1px rgba(139,92,246,0.3) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3f3f46 !important;
}

/* Radio buttons */
div[role="radiogroup"] {
    gap: 8px !important;
    flex-wrap: wrap !important;
}
div[role="radiogroup"] label {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    color: #71717a !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
}
div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(139,92,246,0.12) !important;
    border-color: rgba(139,92,246,0.4) !important;
    color: #e4e4e7 !important;
}

/* Select box */
.stSelectbox > div > div {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e4e4e7 !important;
}

/* Button */
.stButton > button {
    width: 100%;
    padding: 16px !important;
    border-radius: 14px !important;
    border: none !important;
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    color: #fff !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Spinner */
.stSpinner > div {
    color: #a78bfa !important;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #27272a;
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    margin-top: 48px;
    padding-bottom: 24px;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* Hide label for text input */
.stTextInput > label {
    color: #52525b !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-family: 'Space Mono', monospace !important;
}
.stRadio > label, .stSelectbox > label {
    color: #52525b !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-family: 'Space Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS = {
    "ChatGPT": {"color": "#10a37f", "icon": "⬡"},
    "Claude": {"color": "#d97706", "icon": "◈"},
    "Gemini": {"color": "#4285f4", "icon": "✦"},
    "Grok": {"color": "#ef4444", "icon": "✕"},
}

MEDIA_TYPES = ["✎ Text", "◻ Image", "♫ Audio", "▶ Video"]
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
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="text-align:center; padding-top:8px;">
    <span class="hero-badge">✨ Prompt Optimizer</span>
    <div class="hero-title">One Word In.<br>Super Prompt Out.</div>
    <p class="hero-sub">Transform any short idea into a detailed, tool-optimized prompt</p>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT FORM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
user_input = st.text_input(
    "💡 YOUR IDEA",
    placeholder="Type anything... sunset, dragon, coffee shop, AI tutor...",
    key="prompt_input",
)

col1, col2 = st.columns(2)

with col1:
    media_choice = st.radio(
        "📦 OUTPUT TYPE",
        MEDIA_TYPES,
        horizontal=True,
        key="media_type",
    )

with col2:
    tone = st.selectbox("🎭 TONE", TONES, key="tone")

tool = st.radio(
    "🤖 OPTIMIZE FOR",
    list(TOOLS.keys()),
    horizontal=True,
    key="tool",
)

media_type = MEDIA_MAP[media_choice]

# Generate button
generate = st.button(
    f"⚡ Generate {media_type} Prompt for {tool}",
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
            st.error("⚠️ GROQ_API_KEY not found. Add it in Streamlit Secrets (Settings → Secrets).")
        else:
            with st.spinner("⚡ Optimizing your prompt..."):
                try:
                    system_prompt = build_system_prompt(media_type, tool, tone)
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f'Expand this into a detailed super-prompt: "{user_input.strip()}"'},
                        ],
                        max_tokens=1024,
                        temperature=0.8,
                    )
                    result = response.choices[0].message.content
                    word_count = len(result.split())
                    char_count = len(result)

                    # Store in session
                    st.session_state["last_result"] = result
                    st.session_state["last_meta"] = {
                        "tool": tool,
                        "media": media_type,
                        "tone": tone,
                        "words": word_count,
                        "chars": char_count,
                        "input": user_input.strip(),
                    }

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULT DISPLAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    meta = st.session_state["last_meta"]

    st.markdown("---")

    st.markdown(f"""
    <div class="section-card">
        <div class="result-header">
            <span class="section-label" style="margin:0;">Optimized Prompt</span>
            <span class="tag tag-tool">{meta["tool"]}</span>
            <span class="tag tag-media">{meta["media"]}</span>
        </div>
        <div class="result-box">{result}</div>
        <div class="result-meta">
            <span>{meta["words"]} words · {meta["chars"]} chars · "{meta["input"]}"</span>
            <span>Powered by Llama 3.3 via Groq</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Copy button (Streamlit's code block has a built-in copy)
    st.code(result, language=None)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="footer-text">
    Free Forever · Groq API + Streamlit Cloud<br>
    No sign-up needed · No GPU required
</div>
""", unsafe_allow_html=True)
