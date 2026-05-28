"""
utils/rag.py
───────────────────────────────────────────────────────────────────────────────
ToolHaive AI — RAG (Retrieval-Augmented Generation) Engine
Provides ingest, embed, and retrieve functions using ChromaDB (local vector
store) and Ollama's nomic-embed-text embedding model.

Setup (run once):
    pip install chromadb
    ollama pull nomic-embed-text

Usage pattern:
    # One-time ingestion (call from an admin page or script)
    from utils.rag import ingest_text
    ingest_text("fact_checker", "your document text here", doc_id="doc1")

    # At query time (inside any tool page)
    from utils.rag import retrieve
    context = retrieve("fact_checker", user_query)
    # Then inject context into the system prompt before calling chat()
───────────────────────────────────────────────────────────────────────────────
"""

import os
import requests

# ── ChromaDB ──────────────────────────────────────────────────────────────────
# Lazy import so the app still boots if chromadb isn't installed yet.
try:
    import chromadb
    _CHROMA_AVAILABLE = True
except ImportError:
    _CHROMA_AVAILABLE = False

CHROMA_PATH   = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
EMBED_MODEL   = "nomic-embed-text"
OLLAMA_EMBED  = "http://localhost:11434/api/embeddings"

# ── Internal helpers ──────────────────────────────────────────────────────────

def _chroma_client():
    """Return a persistent ChromaDB client, or raise a clear error."""
    if not _CHROMA_AVAILABLE:
        raise ImportError(
            "chromadb is not installed. Run: pip install chromadb"
        )
    return chromadb.PersistentClient(path=CHROMA_PATH)


def _embed(text: str) -> list[float]:
    """Embed a single string using Ollama's nomic-embed-text model."""
    try:
        r = requests.post(
            OLLAMA_EMBED,
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["embedding"]
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Could not connect to Ollama for embeddings. "
            "Make sure Ollama is running (`ollama serve`) and "
            "nomic-embed-text is pulled (`ollama pull nomic-embed-text`)."
        )


def _chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for better retrieval coverage."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]


# ── Public API ────────────────────────────────────────────────────────────────

def ingest_text(
    collection_name: str,
    text: str,
    doc_id: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> int:
    """
    Chunk, embed, and store a document in the named ChromaDB collection.

    Args:
        collection_name: Logical name for this knowledge base
                         (e.g. "fact_checker", "interview_coach").
        text:            The raw document text to ingest.
        doc_id:          A unique identifier for this document
                         (used to namespace chunk IDs).
        chunk_size:      Characters per chunk (default 500).
        overlap:         Character overlap between consecutive chunks (default 50).

    Returns:
        Number of chunks ingested.
    """
    col    = _chroma_client().get_or_create_collection(collection_name)
    chunks = _chunk(text, chunk_size, overlap)
    ids    = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

    col.add(
        ids        = ids,
        documents  = chunks,
        embeddings = [_embed(c) for c in chunks],
    )
    return len(chunks)


def ingest_file(
    collection_name: str,
    file_path: str,
    doc_id: str | None = None,
    chunk_size: int = 500,
    overlap: int = 50,
) -> int:
    """
    Read a plain-text or pre-extracted text file and ingest it.

    For PDFs use pdfplumber to extract text first, then call ingest_text().

    Args:
        collection_name: Target ChromaDB collection.
        file_path:       Absolute or relative path to a .txt file.
        doc_id:          Defaults to the file's base name without extension.
        chunk_size:      Characters per chunk.
        overlap:         Character overlap between chunks.

    Returns:
        Number of chunks ingested.
    """
    doc_id = doc_id or os.path.splitext(os.path.basename(file_path))[0]
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    return ingest_text(collection_name, text, doc_id, chunk_size, overlap)


def retrieve(
    collection_name: str,
    query: str,
    top_k: int = 3,
) -> str:
    """
    Embed the query, find the top-K most similar chunks, and return them
    as a single newline-separated string ready to inject into a system prompt.

    Returns an empty string if the collection does not exist or is empty,
    so callers can safely skip augmentation when no data has been ingested.
    """
    try:
        client = _chroma_client()
        # get_collection raises if collection does not exist
        col = client.get_collection(collection_name)
    except Exception:
        return ""

    try:
        results = col.query(
            query_embeddings=[_embed(query)],
            n_results=min(top_k, col.count()),
        )
        chunks = results.get("documents", [[]])[0]
        return "\n\n---\n\n".join(chunks) if chunks else ""
    except Exception:
        return ""


def collection_exists(collection_name: str) -> bool:
    """Return True if the named collection exists and has at least one document."""
    try:
        col = _chroma_client().get_collection(collection_name)
        return col.count() > 0
    except Exception:
        return False


def delete_collection(collection_name: str) -> None:
    """Delete a collection and all its vectors. Useful for re-ingestion."""
    try:
        _chroma_client().delete_collection(collection_name)
    except Exception:
        pass
