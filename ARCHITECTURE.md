---

## 4. Key Components

### 4.1 RAG (Retrieval-Augmented Generation)

- **Dataset:** King James Version (KJV) Bible
- Each verse is embedded using SentenceTransformers (`all-MiniLM-L6-v2`)
- Query is converted into vector space
- Cosine similarity is used to retrieve top-k relevant verses
- Retrieved verses are injected into LLM prompt for grounding

**Purpose:**
- Prevent hallucinated scripture references
- Improve theological accuracy
- Ensure answers are Bible-grounded

---

### 4.2 Large Language Model (LLM)

- **Model:** LLaMA 3 (Groq API)
- **Role:**
  - Interpret user query
  - Generate natural language response
  - Use retrieved scripture context

Prompt is constrained to:
- Avoid fabricating verses
- Maintain neutrality across denominations
- Provide respectful theological explanations

---

### 4.3 Image Generation Module

- **Model:** FLUX (via Replicate API)
- Generates Christian-themed images from text prompts
- Safety layer blocks:
  - Violent prompts
  - Extremist prompts
  - Religiously harmful prompts

---

### 4.4 Safety Layer

Two-layer safety system:

1. Keyword-based prompt filtering (pre-generation)
2. Model-level moderation (image API refusal)

**Purpose:**
- Prevent extremist religious outputs
- Avoid hateful or violent religious content

---

### 4.5 Intent Detection

Simple rule-based classifier:

- Detects whether input is:
  - Text-based theological question
  - Image generation request
- Routes request accordingly

---

### 4.6 Conversation Memory

- Streamlit session state stores chat history
- Maintains conversational context for LLM
- Enables multi-turn dialogue

---

## 5. Design Decisions

- SentenceTransformers used for lightweight local embedding generation
- Precomputed embeddings stored as `.npy` for efficiency
- Groq used for fast LLM inference
- Replicate used for multimodal image generation
- Streamlit used for rapid UI development

---

## 6. Limitations

- Retrieval quality depends on KJV archaic language alignment
- No advanced reranking (BM25 / cross-encoder not used)
- Simple keyword-based intent detection
- No persistent database (session-only memory)

---

## 7. Future Improvements

- FAISS-based vector search for scalability
- Hybrid retrieval (BM25 + embeddings)
- Fine-tuned theological response model
- Multi-denomination knowledge tagging
- Stronger moderation classifier
- Deployment on cloud (AWS / HF Spaces)