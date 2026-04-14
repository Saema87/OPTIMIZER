import { useState, useRef, useEffect } from "react";

const TOOLS = [
  { id: "chatgpt", label: "ChatGPT" },
  { id: "claude", label: "Claude" },
  { id: "gemini", label: "Gemini" },
  { id: "grok", label: "Grok" },
];

const MEDIA = [
  { id: "text", label: "✎ Text" },
  { id: "image", label: "◻ Image" },
  { id: "audio", label: "♫ Audio" },
  { id: "video", label: "▶ Video" },
];

const TONES = ["Professional", "Creative", "Casual", "Academic", "Persuasive", "Technical"];

function buildSystemPrompt(mediaType, tool, tone) {
  const toolH = {
    chatgpt: "Optimize for OpenAI ChatGPT / DALL-E. Use ChatGPT-style prompt patterns. For images, use DALL-E best practices. For text, leverage system instructions and structured output hints.",
    claude: "Optimize for Anthropic Claude. Use Claude-style patterns with XML tags, clear task decomposition, and explicit constraints.",
    gemini: "Optimize for Google Gemini. Use clear instructions, examples, and Imagen-compatible patterns for images.",
    grok: "Optimize for xAI Grok / Aurora. Use direct instructions with vivid descriptive language and art style references.",
  };
  const mediaH = {
    text: "Generate a detailed text generation super-prompt. Include: role/persona, context, task, format, constraints, tone, example structure.",
    image: "Generate a detailed image generation super-prompt. Include: subject, composition, art style, lighting, color palette, mood, camera angle, negative prompts, aspect ratio.",
    audio: "Generate a detailed audio generation super-prompt. Include: genre, mood, tempo, instruments, vocal style, duration, structure, production quality.",
    video: "Generate a detailed video generation super-prompt. Include: scene, camera movement, duration, visual style, transitions, pacing, color grading, cinematic references.",
  };
  return `You are a world-class prompt engineer. Take a short input and transform it into a highly detailed, optimized super-prompt.\n\n${toolH[tool]}\n\n${mediaH[mediaType]}\n\nTone: ${tone}\n\nRULES:\n- Output ONLY the expanded super-prompt, nothing else\n- No preamble, no explanation, no markdown\n- Be specific, vivid, actionable\n- 150-400 words\n- If input is one word, infer the best interpretation`;
}

export default function App() {
  const [input, setInput] = useState("");
  const [tool, setTool] = useState("chatgpt");
  const [media, setMedia] = useState("text");
  const [tone, setTone] = useState("Professional");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const resRef = useRef(null);

  useEffect(() => {
    if (result && resRef.current) resRef.current.scrollIntoView({ behavior: "smooth" });
  }, [result]);

  const generate = async () => {
    if (!input.trim()) return;
    setLoading(true); setError(""); setResult("");
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: buildSystemPrompt(media, tool, tone),
          messages: [{ role: "user", content: `Expand this into a detailed super-prompt: "${input.trim()}"` }],
        }),
      });
      const data = await res.json();
      if (data.error) setError(data.error.message);
      else setResult(data.content?.map(b => b.text || "").join("") || "");
    } catch { setError("Network error."); }
    finally { setLoading(false); }
  };

  const copy = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const tl = TOOLS.find(t => t.id === tool);
  const ml = MEDIA.find(m => m.id === media);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#f0f4ff",
      fontFamily: "'Outfit', sans-serif",
      position: "relative",
      overflow: "hidden",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

      {/* Gradient mesh */}
      <div style={{ position:"fixed",top:0,left:0,right:0,bottom:0,
        background: `
          radial-gradient(ellipse 600px 500px at 15% 20%, rgba(168,130,255,0.25), transparent),
          radial-gradient(ellipse 500px 600px at 85% 15%, rgba(99,200,255,0.22), transparent),
          radial-gradient(ellipse 700px 400px at 50% 80%, rgba(255,170,200,0.18), transparent),
          radial-gradient(ellipse 400px 400px at 75% 60%, rgba(160,255,200,0.15), transparent)
        `, pointerEvents:"none", zIndex:0 }} />

      {/* Animated blobs */}
      {[
        { w:350,h:350,bg:"linear-gradient(135deg,#c084fc,#818cf8)",t:"-80px",l:"-60px",d:"0s" },
        { w:280,h:280,bg:"linear-gradient(135deg,#67e8f9,#6ee7b7)",t:"30%",r:"-80px",d:"-7s" },
        { w:320,h:320,bg:"linear-gradient(135deg,#fda4af,#fdba74)",b:"-60px",l:"20%",d:"-14s" },
      ].map((b,i) => (
        <div key={i} style={{
          position:"fixed", width:b.w, height:b.h, borderRadius:"50%",
          background:b.bg, filter:"blur(80px)", opacity:0.4,
          top:b.t, left:b.l, right:b.r, bottom:b.b,
          pointerEvents:"none", zIndex:0,
          animation: `blobFloat 20s ease-in-out infinite`,
          animationDelay: b.d,
        }} />
      ))}

      <div style={{ position:"relative", zIndex:1, maxWidth:720, margin:"0 auto", padding:"32px 20px 60px" }}>

        {/* Hero */}
        <div style={{ textAlign:"center", marginBottom:36 }}>
          <span style={{
            display:"inline-flex", alignItems:"center", gap:8,
            background:"rgba(255,255,255,0.6)", backdropFilter:"blur(16px)",
            border:"1px solid rgba(255,255,255,0.8)", borderRadius:100,
            padding:"8px 22px", fontSize:11, letterSpacing:2.5,
            textTransform:"uppercase", color:"#7c3aed",
            fontFamily:"'JetBrains Mono',monospace", fontWeight:500,
            boxShadow:"0 2px 12px rgba(124,58,237,0.08)",
          }}>✨ prompt optimizer</span>
          <h1 style={{
            fontSize:"clamp(30px,5.5vw,48px)", fontWeight:800, lineHeight:1.08,
            background:"linear-gradient(135deg,#1e1b4b 0%,#7c3aed 50%,#2563eb 100%)",
            WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent",
            margin:"20px 0 10px", letterSpacing:-0.5,
          }}>One Word In.<br/>Super Prompt Out.</h1>
          <p style={{ color:"#6b7280", fontSize:16, margin:0 }}>
            Transform any short idea into a detailed, tool‑optimized prompt
          </p>
        </div>

        {/* Glass Card — Input */}
        <Glass style={{ marginBottom:16 }}>
          <Label>💡 your idea</Label>
          <input value={input} onChange={e=>setInput(e.target.value)}
            onKeyDown={e => e.key==="Enter" && generate()}
            placeholder="Type anything… sunset, dragon, coffee shop, AI tutor…"
            style={{
              width:"100%", background:"rgba(255,255,255,0.5)",
              backdropFilter:"blur(12px)", border:"1px solid rgba(255,255,255,0.7)",
              borderRadius:14, padding:"15px 18px", color:"#1f2937",
              fontSize:16, fontFamily:"'Outfit',sans-serif", outline:"none",
              boxSizing:"border-box", boxShadow:"0 2px 12px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.8)",
              transition:"all 0.3s",
            }}
            onFocus={e => { e.target.style.borderColor="rgba(124,58,237,0.4)"; e.target.style.boxShadow="0 0 0 3px rgba(124,58,237,0.1),0 4px 20px rgba(124,58,237,0.08)"; }}
            onBlur={e => { e.target.style.borderColor="rgba(255,255,255,0.7)"; e.target.style.boxShadow="0 2px 12px rgba(0,0,0,0.04),inset 0 1px 0 rgba(255,255,255,0.8)"; }}
          />
        </Glass>

        {/* Media Type */}
        <Glass style={{ marginBottom:16 }}>
          <Label>📦 output type</Label>
          <Chips items={MEDIA} selected={media} onSelect={setMedia} field="id" labelField="label" />
        </Glass>

        {/* Tool */}
        <Glass style={{ marginBottom:16 }}>
          <Label>🤖 optimize for</Label>
          <Chips items={TOOLS} selected={tool} onSelect={setTool} field="id" labelField="label" />
        </Glass>

        {/* Tone */}
        <Glass style={{ marginBottom:24 }}>
          <Label>🎭 tone</Label>
          <div style={{ display:"flex", flexWrap:"wrap", gap:8 }}>
            {TONES.map(t => (
              <button key={t} onClick={() => setTone(t)} style={{
                background: tone===t ? "rgba(124,58,237,0.1)" : "rgba(255,255,255,0.45)",
                backdropFilter:"blur(12px)",
                border: `1px solid ${tone===t ? "rgba(124,58,237,0.35)" : "rgba(255,255,255,0.6)"}`,
                borderRadius:100, padding:"8px 18px", cursor:"pointer",
                fontSize:12.5, fontWeight: tone===t ? 600 : 500,
                color: tone===t ? "#7c3aed" : "#6b7280",
                fontFamily:"'Outfit',sans-serif", transition:"all 0.25s",
                boxShadow: tone===t ? "0 4px 16px rgba(124,58,237,0.1)" : "0 2px 8px rgba(0,0,0,0.03)",
              }}>{t}</button>
            ))}
          </div>
        </Glass>

        {/* Generate */}
        <button onClick={generate} disabled={loading || !input.trim()} style={{
          width:"100%", padding:17, borderRadius:16, border:"none", cursor: loading||!input.trim() ? "not-allowed" : "pointer",
          background:"linear-gradient(135deg,#8b5cf6 0%,#6366f1 50%,#3b82f6 100%)",
          color:"#fff", fontSize:15, fontWeight:600, fontFamily:"'Outfit',sans-serif",
          letterSpacing:0.3, transition:"all 0.3s",
          boxShadow:"0 8px 28px rgba(124,58,237,0.25),0 2px 8px rgba(124,58,237,0.15)",
          opacity: !input.trim() ? 0.5 : 1, marginBottom:24,
        }}>
          {loading ? "✨ Crafting your super prompt…" : `⚡  Generate ${ml.label.slice(2)} Prompt → ${tl.label}`}
        </button>

        {error && <div style={{
          background:"rgba(254,226,226,0.7)", backdropFilter:"blur(12px)",
          border:"1px solid rgba(239,68,68,0.2)", borderRadius:14,
          padding:"14px 18px", marginBottom:16, color:"#b91c1c", fontSize:13,
        }}>{error}</div>}

        {/* Result */}
        {result && (
          <div ref={resRef} style={{
            background:"rgba(255,255,255,0.65)", backdropFilter:"blur(28px)",
            border:"1px solid rgba(124,58,237,0.15)", borderRadius:20,
            padding:28, boxShadow:"0 12px 40px rgba(124,58,237,0.08),inset 0 1px 0 rgba(255,255,255,0.9)",
            animation:"slideUp 0.5s ease-out",
          }}>
            <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:16, flexWrap:"wrap", gap:8 }}>
              <div style={{ display:"flex", alignItems:"center", gap:10, flexWrap:"wrap" }}>
                <span style={{ fontSize:10.5, textTransform:"uppercase", letterSpacing:2, color:"#9ca3af", fontFamily:"'JetBrains Mono',monospace", fontWeight:500 }}>optimized prompt</span>
                <Tag bg="rgba(124,58,237,0.1)" color="#7c3aed" border="rgba(124,58,237,0.15)">{tl.label}</Tag>
                <Tag bg="rgba(59,130,246,0.08)" color="#3b82f6" border="rgba(59,130,246,0.12)">{ml.label.slice(2)}</Tag>
                <Tag bg="rgba(16,185,129,0.08)" color="#059669" border="rgba(16,185,129,0.12)">{tone}</Tag>
              </div>
              <button onClick={copy} style={{
                background: copied ? "rgba(16,185,129,0.12)" : "rgba(255,255,255,0.5)",
                backdropFilter:"blur(12px)", border:`1px solid ${copied ? "rgba(16,185,129,0.3)" : "rgba(255,255,255,0.6)"}`,
                borderRadius:10, padding:"8px 16px", cursor:"pointer",
                fontSize:12, fontWeight:500, color: copied ? "#059669" : "#6b7280",
                fontFamily:"'Outfit',sans-serif", transition:"all 0.3s",
              }}>{copied ? "✓ Copied!" : "Copy"}</button>
            </div>
            <div style={{
              background:"rgba(255,255,255,0.5)", backdropFilter:"blur(12px)",
              border:"1px solid rgba(255,255,255,0.6)", borderRadius:14,
              padding:22, fontSize:14.5, lineHeight:1.8, color:"#374151",
              whiteSpace:"pre-wrap", wordBreak:"break-word",
              fontFamily:"'Outfit',sans-serif", maxHeight:420, overflowY:"auto",
              boxShadow:"inset 0 2px 8px rgba(0,0,0,0.03)",
            }}>{result}</div>
            <div style={{ display:"flex", justifyContent:"space-between", marginTop:12, fontSize:11, color:"#9ca3af", fontFamily:"'JetBrains Mono',monospace" }}>
              <span>{result.split(/\s+/).length} words · {result.length} chars</span>
              <span>powered by claude</span>
            </div>
          </div>
        )}

        <div style={{ textAlign:"center", marginTop:48, color:"#b0b8c8", fontSize:11, fontFamily:"'JetBrains Mono',monospace", letterSpacing:0.5 }}>
          free forever · groq api + streamlit cloud · no sign‑up · no gpu
        </div>
      </div>

      <style>{`
        @keyframes blobFloat {
          0%,100% { transform: translate(0,0) scale(1); }
          25% { transform: translate(30px,-40px) scale(1.05); }
          50% { transform: translate(-20px,20px) scale(0.95); }
          75% { transform: translate(15px,35px) scale(1.03); }
        }
        @keyframes slideUp {
          from { opacity:0; transform:translateY(16px); }
          to { opacity:1; transform:translateY(0); }
        }
        * { box-sizing:border-box; }
        input::placeholder { color:#b0b8c8; }
      `}</style>
    </div>
  );
}

function Glass({ children, style }) {
  return (
    <div style={{
      background:"rgba(255,255,255,0.55)", backdropFilter:"blur(24px)",
      WebkitBackdropFilter:"blur(24px)",
      border:"1px solid rgba(255,255,255,0.7)", borderRadius:20,
      padding:"24px 28px",
      boxShadow:"0 8px 32px rgba(100,100,180,0.08),inset 0 1px 0 rgba(255,255,255,0.8)",
      ...style,
    }}>{children}</div>
  );
}

function Label({ children }) {
  return (
    <div style={{
      fontSize:10.5, textTransform:"uppercase", letterSpacing:2,
      color:"#9ca3af", fontFamily:"'JetBrains Mono',monospace",
      fontWeight:500, marginBottom:12,
    }}>{children}</div>
  );
}

function Chips({ items, selected, onSelect, field, labelField }) {
  return (
    <div style={{ display:"flex", flexWrap:"wrap", gap:10 }}>
      {items.map(it => {
        const active = it[field] === selected;
        return (
          <button key={it[field]} onClick={() => onSelect(it[field])} style={{
            background: active ? "rgba(124,58,237,0.1)" : "rgba(255,255,255,0.45)",
            backdropFilter:"blur(12px)",
            border: `1px solid ${active ? "rgba(124,58,237,0.35)" : "rgba(255,255,255,0.6)"}`,
            borderRadius:12, padding:"11px 22px", cursor:"pointer",
            fontSize:13, fontWeight: active ? 600 : 500,
            color: active ? "#7c3aed" : "#6b7280",
            fontFamily:"'Outfit',sans-serif", transition:"all 0.25s",
            boxShadow: active ? "0 4px 16px rgba(124,58,237,0.1)" : "0 2px 8px rgba(0,0,0,0.03)",
          }}>{it[labelField]}</button>
        );
      })}
    </div>
  );
}

function Tag({ children, bg, color, border }) {
  return (
    <span style={{
      padding:"4px 14px", borderRadius:100, fontSize:11,
      fontWeight:600, fontFamily:"'Outfit',sans-serif",
      background:bg, color, border:`1px solid ${border}`,
    }}>{children}</span>
  );
}
