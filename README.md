---
title: SLD AI Explainer
emoji: ⚡
colorFrom: yellow
colorTo: slate
sdk: gradio
sdk_version: "4.36.0"
app_file: app.py
pinned: true
---

# ⚡ SLD AI Explainer

**Intelligent Single Line Diagram Analyzer for Electrical Engineers**

An AI-powered tool that analyzes electrical Single Line Diagrams (SLDs) — solar plants, substations, distribution networks — and provides instant, expert-level explanations.

---

## 🚀 Features

| Mode | What it does |
|---|---|
| 🔍 Full Explanation | Complete breakdown of all components, power flow, and protection devices |
| ⚠️ Fault Diagnosis | Describe a fault symptom → AI identifies root cause and suggests fixes |
| 🔎 Component Lookup | Type a component name → AI finds and explains it in your diagram |

---

## 🛠️ Tech Stack

- **Python** — core language
- **Gradio** — UI framework, deployed on Hugging Face Spaces
- **Anthropic Claude API** — vision + language model for diagram analysis
- **claude-opus-4-6** — multimodal model with image understanding

---

## 💻 Run Locally
'''bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sld-ai-explainer.git
cd sld-ai-explainer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
# Windows (Command Prompt):
set GEMINI_API_KEY=your_key_here

# Windows (PowerShell):
$env:GEMINI_API_KEY="your_key_here"

# 4. Run
python app.py
'''
Then open **http://localhost:7860** in your browser.

---

## 🌐 Deploy on Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Gradio** as the SDK
3. Upload `app.py` and `requirements.txt`
4. Go to **Settings → Variables and Secrets** → add `ANTHROPIC_API_KEY`
5. Your app goes live automatically!

---

## 👤 Author

**Tahir Abbas**  
Electrical Engineer | AI Developer | O&M Engineer at Nizam Energy Pvt Ltd  
📧 ee.tahirabbas@gmail.com

*Built as part of PEC × PakAngels Generative AI Training Program*

---

## 📄 License

MIT License
