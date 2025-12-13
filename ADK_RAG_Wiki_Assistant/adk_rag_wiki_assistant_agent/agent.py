import os
from typing import List, Tuple

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import numpy as np
from openai import OpenAI

from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

# ---------------------------------------------------------
# Environment & clients
# ---------------------------------------------------------

load_dotenv()

WIKI_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment or .env file.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"  # cheap and good


# ---------------------------------------------------------
# Helper: fetch and parse Wikipedia content
# ---------------------------------------------------------

def fetch_wiki_content() -> str:
    """Fetch and clean the main content of the Artificial Intelligence Wikipedia page."""
    try:
        print(f"Fetching content from: {WIKI_URL}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(WIKI_URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            print("Could not find main content div on the page.")
            return ""

        paragraphs = content_div.find_all("p")
        text_chunks = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                text_chunks.append(text)

        full_text = "\n".join(text_chunks)
        print(f"Fetched {len(text_chunks)} paragraphs from Wikipedia.")
        return full_text

    except Exception as e:
        print(f"Error fetching Wikipedia content: {e}")
        return ""


# ---------------------------------------------------------
# Helper: chunking
# ---------------------------------------------------------

def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """Split long text into chunks of at most max_chars, respecting paragraph boundaries."""
    paragraphs = text.split("\n")
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if not para.strip():
            continue

        if len(current) + len(para) + 1 <= max_chars:
            current += (" " if current else "") + para
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks


# ---------------------------------------------------------
# Helper: embeddings
# ---------------------------------------------------------

def embed_texts(texts: List[str]) -> np.ndarray:
    """Get OpenAI embeddings for a list of texts. Returns an array of shape (n, d)."""
    if not texts:
        return np.zeros((0, 1), dtype=np.float32)

    print(f"[embed_texts] Embedding {len(texts)} texts with {EMBEDDING_MODEL}...")

    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    vectors = [np.array(item.embedding, dtype=np.float32) for item in response.data]
    return np.vstack(vectors)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between each row of a and a single vector b."""
    # a: (n, d), b: (d,)
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-10)
    b_norm = b / (np.linalg.norm(b) + 1e-10)
    return np.dot(a_norm, b_norm)


# ---------------------------------------------------------
# Simple in-memory embedding store (cached for this process)
# ---------------------------------------------------------

_EMBEDDING_CACHE = {
    "chunks": None,       # type: List[str] | None
    "embeddings": None,   # type: np.ndarray | None
}


def build_or_get_embedding_index() -> Tuple[List[str], np.ndarray]:
    """Fetch content, chunk it, and build (or reuse) an embedding index."""
    if _EMBEDDING_CACHE["chunks"] is not None and _EMBEDDING_CACHE["embeddings"] is not None:
        print("[build_or_get_embedding_index] Using cached embeddings.")
        return _EMBEDDING_CACHE["chunks"], _EMBEDDING_CACHE["embeddings"]

    print("[build_or_get_embedding_index] Building embeddings from scratch...")
    content = fetch_wiki_content()
    if not content:
        return [], np.zeros((0, 1), dtype=np.float32)

    chunks = chunk_text(content, max_chars=800)
    embeddings = embed_texts(chunks)

    _EMBEDDING_CACHE["chunks"] = chunks
    _EMBEDDING_CACHE["embeddings"] = embeddings

    print(f"[build_or_get_embedding_index] Built {len(chunks)} chunks.")
    return chunks, embeddings


# ---------------------------------------------------------
# RAG search using embeddings
# ---------------------------------------------------------

def embedding_rag_search(query: str, top_k: int = 3) -> str:
    """
    RAG-style retrieval over the AI Wikipedia page using OpenAI embeddings.
    """
    print("====================================================")
    print(f"[embedding_rag_search] Query: {query}")
    print("====================================================")

    chunks, embeddings = build_or_get_embedding_index()
    if len(chunks) == 0:
        return "I couldn't retrieve or index the reference content right now. Please try again later."

    # Embed query
    query_embedding = embed_texts([query])[0]  # shape: (d,)

    # Compute cosine similarity
    sims = cosine_similarity(embeddings, query_embedding)  # shape: (n,)
    ranked_indices = np.argsort(-sims)  # descending

    top_indices = ranked_indices[:top_k]
    print(f"[embedding_rag_search] Top {len(top_indices)} chunks selected.")

    context_pieces = []
    for idx in top_indices:
        score = float(sims[idx])
        chunk = chunks[idx]
        print(f"  - Chunk {idx} | score={score:.4f}")
        context_pieces.append(chunk)

    context = "\n\n".join(context_pieces)
    preview = context[:400].replace("\n", " ")
    print("----------------------------------------------------")
    print(f"[embedding_rag_search] Context preview: {preview}...")
    print("----------------------------------------------------")

    return context


def retrieve_ai_context(query: str) -> str:
    """
    Tool exposed to the agent: retrieve relevant AI context from Wikipedia
    using embedding-based similarity search.
    """
    return embedding_rag_search(query)


# ---------------------------------------------------------
# ADK tool + agent definition
# ---------------------------------------------------------

rag_tool = FunctionTool(func=retrieve_ai_context)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="wiki_rag_embedding_agent",
    description=(
        "An AI assistant that answers questions about Artificial Intelligence "
        "using the Artificial Intelligence Wikipedia page as a reference and "
        "embedding-based retrieval."
    ),
    instruction=(
        "You are a helpful assistant that answers questions about Artificial Intelligence. "
        "For EVERY user question, you MUST first call the `retrieve_ai_context` tool with "
        "the user's query to retrieve relevant context from the AI Wikipedia page. "
        "Then, use ONLY that context (and your general reasoning ability) to produce a "
        "grounded, accurate answer. Do not invent facts that are not supported by the "
        "retrieved context. When appropriate, quote or paraphrase the context clearly."
    ),
    tools=[rag_tool],
)

# IMPORTANT: Do NOT call adk.agent(...) or adk.run(...)
# ADK in your setup auto-discovers `root_agent` from this module.
