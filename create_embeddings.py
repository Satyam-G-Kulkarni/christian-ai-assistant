import json
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD BIBLE DATA
# -----------------------------

with open("data/kjv.json", "r") as f:
    bible_data = json.load(f)

verses = bible_data["verses"]

# -----------------------------
# CREATE DOCUMENTS
# -----------------------------

documents = [
    f"{v['book_name']} {v['chapter']}:{v['verse']} - {v['text']}"
    for v in verses
]

# -----------------------------
# SAVE DOCUMENTS
# -----------------------------

with open("data/documents.json", "w") as f:
    json.dump(documents, f)

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# GENERATE EMBEDDINGS
# -----------------------------

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

# -----------------------------
# SAVE EMBEDDINGS
# -----------------------------

np.save(
    "data/bible_embeddings.npy",
    embeddings
)

print("Embeddings saved successfully.")