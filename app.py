import streamlit as st
from openai import OpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Prompt Optimizer",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MINIMAL CSS — only background + hero + result
# Do NOT override any Streamlit widget styles
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Background gradient mesh */
.stApp {
    background:
        radial-gradient(ellipse 600px 500px at 15% 20%, rgba(168,130,255,0.18), transparent),
        radial-gradient(ellipse 500px 600px at 85% 15%, rgba(99,200,255,0.15), transparent),
        radial-gradient(ellipse 700px 400px at 50% 85%, rgba(255,170,200,0.12), transparent),
        #f0f4ff !important;
}

/* Hide defaults */
#MainMenu, footer { visibility: hidden; }

/* Hero section */
.hero-wrap { text-align: center; padding: 8px 0 24px; }
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(200,200,240,0.4);
    border-radius: 100px;
    padding: 8px 22px;
    font-size: 11px; letter-spacing: 2.5px;
    text-transform: uppercase; color: #7c3aed;
    font-family: 'JetBrains Mono', monospace; font-weight: 500;
}
.hero-title {
    font-size: clamp(28px, 5vw, 46px); font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #1e1b4b 0%, #7c3aed 50%, #2563eb 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 18px 0 8px; font-family: 'Outfit', sans-serif;
}
.hero-sub {
    color: #6b7280; font-size: 15px;
    font-family: 'Outfit', sans-serif;
}

/* Result card */
.result-card {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 16px; padding: 24px; margin: 12px 0;
    box-shadow: 0 8px 30px rgba(124,58,237,0.06);
}
.result-header {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 14px; flex-wrap: wrap;
}
.result-label {
    font-size: 10px; text-transform: uppercase; letter-spacing: 2px;
    color: #9ca3af; font-family: 'JetBrains Mono', monospace; font-weight: 500;
}
.tag {
    display: inline-block; padding: 3px 12px; border-radius: 100px;
    font-size: 11px; font-weight: 600; font-family: 'Outfit', sans-serif;
}
.tag-tool { background: rgba(124,58,237,0.08); color: #7c3aed; }
.tag-media { background: rgba(59,130,246,0.07); color: #3b82f6; }
.tag-tone { background: rgba(16,185,129,0.07); color: #059669; }
.result-box {
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(200,200,240,0.3);
    border-radius: 12px; padding: 20px;
    font-size: 14px; line-height: 1.8; color: #374151;
    white-space: pre-wrap; word-break: break-word;
    font-family: 'Outfit', sans-serif;
    max-height: 400px; overflow-y: auto;
}
.result-meta {
    display: flex; justify-content: space-between;
    margin-top: 10px; font-size: 11px; color: #9ca3af;
    font-family: 'JetBrains Mono', monospace;
}
.footer-text {
    text-align: center; color: #b0b8c8; font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 40px; padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS_LIST = ["ChatGPT", "Claude", "Gemini", "Grok"]
MEDIA_DISPLAY = ["✎ Text", "◻ Image", "♫ Audio", "▶ Video"]
MEDIA_MAP = {
    "✎ Text": "Text",
    "◻ Image": "Image",
    "♫ Audio": "Audio",
    "▶ Video": "Video",
}
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
# INPUT CONTROLS — using native Streamlit widgets
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
user_input = st.text_input(
    "💡 Your Idea",
    placeholder="Type anything… sunset, dragon, coffee shop, AI tutor…",
)

col1, col2 = st.columns(2)
with col1:
    media_choice = st.radio("📦 Output Type", MEDIA_DISPLAY, horizontal=True)
with col2:
    tone = st.selectbox("🎭 Tone", TONES)

tool = st.radio("🤖 Optimize For", TOOLS_LIST, horizontal=True)

media_type = MEDIA_MAP[media_choice]

generate = st.button(
    f"⚡ Generate {media_type} Prompt → {tool}",
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
            st.error("⚠️ GROQ_API_KEY not found in Secrets. Go to app Settings → Secrets and add your key.")
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
                    st.error(f"❌ Error: {str(e)}")


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
        <span class="result-label">OPTIMIZED PROMPT</span>
        <span class="tag tag-tool">{m["tool"]}</span>
        <span class="tag tag-media">{m["media"]}</span>
        <span class="tag tag-tone">{m["tone"]}</span>
    </div>
    <div class="result-box">{r}</div>
    <div class="result-meta">
        <span>{m["words"]} words · {m["chars"]} chars · "{m["input"]}"</span>
        <span>Llama 3.3 70B via Groq</span>
    </div>
</div>
""", unsafe_allow_html=True)

    # Native Streamlit code block with built-in copy button
    st.code(r, language=None)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="footer-text">Free Forever · Groq API + Streamlit Cloud · No sign‑up · No GPU</div>', unsafe_allow_html=True)
