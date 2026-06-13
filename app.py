import gradio as gr
import google.generativeai as genai
import os
from pathlib import Path
from PIL import Image

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """You are an expert Electrical Engineer specializing in power systems and solar energy.
Analyze Single Line Diagrams (SLDs) concisely and clearly.

IMPORTANT: Keep your response SHORT and scannable. Use bullet points. No long paragraphs.

Format EXACTLY like this:

## 📋 Overview
One sentence describing the system type and purpose.

## ⚡ Key Components
- **Component name** — what it does (1 line each)
- List only the most important ones (max 6-8)

## 🔄 Power Flow
Source → Step 1 → Step 2 → Load (keep it to 2-3 lines)

## 🛡️ Protection Devices
- List protection/safety devices only (skip if none visible)

## 💡 Notable Points
- 2-3 bullet points of anything important or unusual

Total response should be under 300 words."""

def analyze_sld(image_path, user_question, mode):
    if image_path is None:
        return "⚠️ Please upload an SLD image first."
    try:
        image = Image.open(image_path)

        if mode == "🔍 Full Explanation":
            q = user_question.strip() if user_question.strip() else "Analyze this SLD concisely."
            prompt = f"{SYSTEM_PROMPT}\n\nTask: {q}"

        elif mode == "⚠️ Fault Diagnosis":
            if not user_question.strip():
                return "⚠️ Describe the fault or symptom in the text box below."
            prompt = (f"You are an expert electrical fault diagnosis engineer. Be concise.\n\n"
                      f"SLD fault report: {user_question.strip()}\n\n"
                      f"Respond in this format:\n"
                      f"## 🔴 Likely Cause\n(1-2 sentences)\n\n"
                      f"## 🔧 Affected Components\n- bullet list\n\n"
                      f"## ✅ Corrective Actions\n- numbered steps (max 4)")

        else:  # Component Lookup
            if not user_question.strip():
                return "⚠️ Type the component name you want looked up."
            prompt = (f"Explain this electrical component found in the SLD: **{user_question.strip()}**\n\n"
                      f"Format:\n"
                      f"## Component: {user_question.strip()}\n"
                      f"**Function:** one sentence\n"
                      f"**Symbol:** describe it briefly\n"
                      f"**Ratings visible:** (if any)\n"
                      f"**Why it matters:** one sentence")

        response = model.generate_content([prompt, image])
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}\n\nCheck that your GEMINI_API_KEY is set."


CSS = """
/* ── Reset & Base ── */
body, .gradio-container { background: #111827 !important; color: #e2e8f0 !important; }
.gradio-container { max-width: 1000px !important; margin: auto !important; font-family: 'Inter', sans-serif !important; }

/* ── Header ── */
#app-header {
    background: #1e2d4f;
    border: 1px solid #2e4a80;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    text-align: center;
}
#app-header h1 { color: #60a5fa !important; font-size: 2rem !important; margin: 0 0 6px !important; }
#app-header p { color: #cbd5e1 !important; margin: 0 !important; font-size: 0.95rem !important; }

/* ── Panels ── */
.panel-left, .panel-right {
    background: #1a2540 !important;
    border: 1px solid #2e4a80 !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* ── Upload area ── */
.upload-zone {
    border: 2px dashed #3b5fa0 !important;
    border-radius: 12px !important;
    background: #131f35 !important;
    min-height: 200px !important;
    color: #94a3b8 !important;
}

/* ── Labels ── */
label, .gr-form > label, span.svelte-1gfkn6j {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Radio buttons — fix white bg ── */
fieldset, .gr-form { background: transparent !important; border: none !important; }
.gr-radio-row { gap: 8px !important; }
input[type="radio"] + span, input[type="radio"] ~ span {
    background: #1e3560 !important;
    border: 1px solid #2e4a80 !important;
    border-radius: 8px !important;
    color: #cbd5e1 !important;
    padding: 8px 14px !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}
input[type="radio"]:checked + span, input[type="radio"]:checked ~ span {
    background: #1d4ed8 !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;
}

/* ── Textbox ── */
textarea {
    background: #131f35 !important;
    border: 1px solid #2e4a80 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.92rem !important;
    padding: 10px 14px !important;
}
textarea::placeholder { color: #6b7fa3 !important; }
textarea:focus { border-color: #3b82f6 !important; outline: none !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important; }

/* ── Analyze button ── */
#analyze-btn {
    background: #1d4ed8 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
#analyze-btn:hover { background: #2563eb !important; transform: translateY(-1px) !important; }
#analyze-btn:active { transform: translateY(0) !important; }

/* ── Result heading ── */
#result-heading p, #result-heading h3 { color: #93c5fd !important; font-size: 1rem !important; font-weight: 600 !important; }

/* ── Output panel ── */
#output-panel {
    background: #131f35 !important;
    border: 1px solid #2e4a80 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    min-height: 300px !important;
    color: #cbd5e1 !important;
    line-height: 1.7 !important;
    font-size: 0.93rem !important;
}
#output-panel p, #output-panel li { color: #cbd5e1 !important; }
#output-panel em { color: #6b7fa3 !important; }
#output-panel h2 { color: #60a5fa !important; font-size: 1rem !important; border-bottom: 1px solid #2e4a80; padding-bottom: 6px; margin-top: 18px !important; }
#output-panel h2:first-child { margin-top: 0 !important; }
#output-panel strong { color: #93c5fd !important; }
#output-panel ul { padding-left: 18px !important; }
#output-panel li { margin-bottom: 4px !important; }

/* ── Accordion ── */
.gr-accordion { background: #1a2540 !important; border: 1px solid #2e4a80 !important; border-radius: 10px !important; }
.gr-accordion button, .gr-accordion span { color: #cbd5e1 !important; }
.gr-accordion .gr-markdown p, .gr-accordion .gr-markdown li { color: #94a3b8 !important; }

/* ── Footer ── */
footer { display: none !important; }
"""

HEADER_HTML = """
<div id="app-header">
  <h1>⚡ SLD AI Explainer</h1>
  <p>Intelligent Single Line Diagram Analyzer &nbsp;|&nbsp; Solar · Substations · Distribution Networks</p>
  <p style="margin-top:8px; font-size:0.85rem; color:#94a3b8;">Built by <strong style="color:#60a5fa;">Tahir Abbas</strong> &nbsp;·&nbsp; Electrical Engineer &amp; AI Developer</p>
</div>
"""

MODES = ["🔍 Full Explanation", "⚠️ Fault Diagnosis", "🔎 Component Lookup"]

with gr.Blocks(css=CSS, title="SLD AI Explainer") as demo:

    gr.HTML(HEADER_HTML)

    with gr.Row(equal_height=False):
        with gr.Column(scale=1, elem_classes="panel-left"):
            image_input = gr.Image(
                type="filepath",
                label="Upload SLD Image",
                sources=["upload", "clipboard"],
                elem_classes="upload-zone",
            )
            mode_selector = gr.Radio(
                choices=MODES,
                value=MODES[0],
                label="Analysis Mode",
            )
            question_input = gr.Textbox(
                label="Question / Fault Description (optional)",
                placeholder="e.g. 'What protection is used?' or 'CB-3 trips at 8AM every day'",
                lines=3,
            )
            analyze_btn = gr.Button("⚡  Analyze SLD", variant="primary", elem_id="analyze-btn")

        with gr.Column(scale=1, elem_classes="panel-right"):
            gr.Markdown("### Analysis Result", elem_id="result-heading")
            output_box = gr.Markdown(
                value="*Upload an SLD image and click Analyze to get started.*",
                elem_id="output-panel",
            )

    with gr.Accordion("ℹ️ How to use this tool", open=False):
        gr.Markdown("""
**Full Explanation** — Uploads any SLD → complete breakdown of components, power flow & protection. Question is optional.

**Fault Diagnosis** — Describe a fault symptom (e.g. *"Breaker CB-3 trips every morning at 08:00"*) → AI identifies the likely cause and fix.

**Component Lookup** — Type a component name (e.g. *"OLTC transformer"* or *"differential relay"*) → instant explanation.

Supported image formats: JPG · PNG · WEBP
        """)

    analyze_btn.click(
        fn=analyze_sld,
        inputs=[image_input, question_input, mode_selector],
        outputs=output_box,
    )

if __name__ == "__main__":
    demo.launch()