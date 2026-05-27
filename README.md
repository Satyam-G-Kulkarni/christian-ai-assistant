# ✝️ Christianity AI Assistant

> A Retrieval-Augmented Generation (RAG) chatbot grounded in the King James Bible — with AI image generation and multi-denomination awareness.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3-orange)
![Replicate](https://img.shields.io/badge/Image-Replicate%20FLUX-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**Christian AI Assistant** is a Streamlit-based chatbot that answers questions through a Biblical lens using RAG (Retrieval-Augmented Generation). It retrieves relevant KJV Bible verses for every query, generates grounded responses via LLaMA 3.3 (Groq), and can produce Christian-themed images using FLUX 1.1 Pro (Replicate).

---

## 🖼️ Demo

> 📸 *Screenshot / GIF placeholder — add your own after running the app locally.*

<!-- Replace the line below with your actual screenshot -->
![Demo Screenshot](assets/demo_placeholder.png)

---

## 🧠 How It Works

```
User Query
    │
    ▼
┌─────────────────────┐
│  Safety Check       │  ← Blocks harmful prompts
└─────────┬───────────┘
          │
    ┌─────┴──────┐
    │            │
    ▼            ▼
Image?        Text?
    │            │
    ▼            ▼
FLUX 1.1    RAG Retrieval
(Replicate)  (KJV Bible)
                 │
                 ▼
          LLaMA 3.3 70B
             (Groq)
                 │
                 ▼
           AI Response
```

---

## ✨ Features

- 📖 **Bible RAG** — Retrieves the top-5 most relevant KJV verses for every question using semantic similarity
- 🤖 **LLaMA 3.3 70B** — Powered by Groq for fast, theologically aware responses
- 🎨 **AI Image Generation** — Generate Christian-themed art via FLUX 1.1 Pro on Replicate
- 🛡️ **Safety Filter** — Blocks harmful or extremist prompts before any API call
- ⛪ **Multi-Denomination Aware** — Respects Catholic, Protestant, and Orthodox perspectives
- 💬 **Chat History** — Full conversational memory within a session
- ⚡ **Precomputed Embeddings** — No recomputation on startup; loads `.npy` directly

---

## 🗂️ Project Structure

```
christian-ai-assistant/
│
├── app.py                    # Main Streamlit application
├── precompute_embeddings.py  # Script to generate bible_embeddings.npy + documents.json
│
├── bible_embeddings.npy      # Precomputed sentence embeddings (31,102 KJV verses)
├── documents.json            # Formatted verse strings for retrieval
├── kjv.json                  # Raw KJV Bible source data
│
├── assets/
│   └── demo_placeholder.png  # Add your own screenshot here
│
├── requirements.txt          # Python dependencies
├── .env.example              # API key template
├── .gitignore                # Git ignore rules
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/christian-ai-assistant.git
cd christian-ai-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
```

Get your keys from:
- **Groq**: [console.groq.com](https://console.groq.com)
- **Replicate**: [replicate.com](https://replicate.com)

### 4. Run the App

```bash
streamlit run app.py
```

---

## 📦 Precomputed Files

This repo includes `bible_embeddings.npy` and `documents.json` so the app starts instantly without recomputing embeddings.

If you want to regenerate them yourself (e.g., with a different embedding model):

```bash
python precompute_embeddings.py
```

> ⚠️ This requires `kjv.json` to be present and takes a few minutes to run.

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| UI Framework | Streamlit |
| Embedding Model | `all-MiniLM-L6-v2` (Sentence Transformers) |
| Vector Search | Scikit-learn Cosine Similarity |
| LLM | LLaMA 3.3 70B Versatile via Groq |
| Image Generation | FLUX 1.1 Pro via Replicate |
| Bible Source | King James Version (KJV) |

---

## ⚙️ Configuration

You can adjust these values in `app.py`:

| Parameter | Default | Description |
|---|---|---|
| `top_k` in `retrieve_verses()` | `5` | Number of Bible verses retrieved per query |
| `model` in Groq call | `llama-3.3-70b-versatile` | LLM model used |
| `max_tokens` | `1000` | Max tokens in LLM response |

---

## 🛡️ Safety & Ethics

- Harmful, violent, or extremist prompts are blocked before reaching any API
- The assistant does not claim any single denomination is the only true Christianity
- Scripture references are grounded in actual retrieved verses — not invented
- Image generation is filtered through the same safety check

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [KJV Bible JSON](https://github.com/aruljohn/Bible-kjv) for the structured Bible data
- [Sentence Transformers](https://www.sbert.net/) for the embedding model
- [Groq](https://groq.com/) for ultra-fast LLM inference
- [Replicate](https://replicate.com/) for FLUX image generation
