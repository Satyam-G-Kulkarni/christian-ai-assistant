import streamlit as st
import os
import json
import numpy as np
import replicate
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# API KEYS
# -----------------------------

os.environ["GROQ_API_KEY"] = "Your Key here"
os.environ["REPLICATE_API_TOKEN"] = "Your Key here"

# -----------------------------
# CLIENTS
# -----------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

replicate_client = replicate.Client(
    api_token=os.getenv("REPLICATE_API_TOKEN")
)

# -----------------------------
# SYSTEM PROMPT
# -----------------------------

system_prompt = """
You are a Christianity-focused AI assistant.

Rules:
- Stay aligned with Biblical principles.
- Do not invent scripture references.
- If uncertain, admit uncertainty.
- Respect Catholic, Protestant, and Orthodox traditions.
- Explain theological differences neutrally.
- Do not claim one denomination is the only true Christianity.
- Avoid extremist or harmful content.
- Be calm, respectful, and grounded.
"""

# -----------------------------
# SAFETY CHECK
# -----------------------------

def is_safe_prompt(prompt):
    blocked_words = [
        "hate", "violence", "genocide",
        "extremist", "terror", "propaganda"
    ]
    p = prompt.lower()
    return not any(w in p for w in blocked_words)

# -----------------------------
# IMAGE DETECTION
# -----------------------------

def is_image_request(text):
    keywords = [
        "generate image",
        "create image",
        "draw",
        "painting",
        "illustration",
        "picture of",
        "art of"
    ]
    t = text.lower()
    return any(k in t for k in keywords)

# -----------------------------
# LOAD BIBLE (RAG)
# -----------------------------

@st.cache_resource
def load_bible():
    with open("documents.json", "r") as f:
        documents = json.load(f)
    return documents


documents = load_bible()

# -----------------------------
# EMBEDDING MODEL
# -----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


embedding_model = load_model()

# -----------------------------
# LOAD EMBEDDINGS FROM FILE
# -----------------------------

@st.cache_resource
def load_embeddings():
    return np.load("bible_embeddings.npy")


all_embeddings = load_embeddings()

# -----------------------------
# RAG RETRIEVAL
# -----------------------------

def retrieve_verses(query, top_k=5):
    q_emb = embedding_model.encode([query])
    sims = cosine_similarity(q_emb, all_embeddings)
    top_idx = np.argsort(sims[0])[-top_k:][::-1]
    return "\n".join([documents[i] for i in top_idx])

# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("Christian AI Assistant (RAG + Image + Chat)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "image":
            st.image(msg["content"])
        else:
            st.write(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------

user_input = st.chat_input("Ask something...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "type": "text"
    })

    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------
    # IMAGE FLOW
    # -----------------------------

    if is_image_request(user_input):

        if is_safe_prompt(user_input):

            try:
                output = replicate_client.run(
                    "black-forest-labs/flux-1.1-pro",
                    input={"prompt": user_input}
                )

                image_url = str(output)

                with st.chat_message("assistant"):
                    st.image(image_url)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": image_url,
                    "type": "image"
                })

            except Exception:
                with st.chat_message("assistant"):
                    st.write("Image generation failed or blocked.")

        else:
            msg = "Unsafe image request detected."

            with st.chat_message("assistant"):
                st.write(msg)

            st.session_state.messages.append({
                "role": "assistant",
                "content": msg,
                "type": "text"
            })

    # -----------------------------
    # TEXT + RAG FLOW
    # -----------------------------

    else:

        # RAG retrieval
        context = retrieve_verses(user_input)

        rag_prompt = system_prompt + f"""

Bible Context:
{context}
"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": rag_prompt}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["type"] == "text"
            ]
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "type": "text"
        })
