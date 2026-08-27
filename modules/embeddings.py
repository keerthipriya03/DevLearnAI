#step 4.1
import streamlit as st
from sentence_transformers import SentenceTransformer
                                                                                #func done by this is
MODEL_NAME = "all-MiniLM-L6-v2"                                                 # load_embedding_model()
                                                                                   #    ↓
@st.cache_resource                                                           # Download/load all-MiniLM-L6-v2
def load_embedding_model():                                                        #    ↓
    return SentenceTransformer(MODEL_NAME)                                       # Keep it cached


def generate_embedding(text):
    model = load_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()

#step4.4
def generate_embeddings(chunks):
    model = load_embedding_model()
    texts = [
        chunk["text"]
        for chunk in chunks
    ]
    embeddings = model.encode(
        texts,
        show_progress_bar=False
    )
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    return chunks
