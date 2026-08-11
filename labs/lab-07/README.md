# Lab 07: RAG Over Node.js Docs

## Why This Lab Exists

This lab is for learning retrieval-augmented generation end to end. The goal is to build a system that answers questions about Node.js docs by retrieving relevant chunks first, then asking the model to answer only from that retrieved context.

## What I Learned On The First Pass

- How to chunk documentation into smaller sections that are still useful to retrieve.
- Why chunk metadata and breadcrumbs help preserve context after splitting a document.
- How to index documentation in a vector database.
- Why retrieval quality matters before generation even starts.
- How grounding the final answer in retrieved docs reduces hallucination.

## Core AI And Tech Topics

- RAG
- Document chunking
- Embeddings
- ChromaDB
- Retrieval and reranking
- Grounded answering

## Folder Structure

```text
lab-07/
├── README.md
├── ask-node.py
├── chunker.py
├── chroma_db/
├── docs/
├── indexer.py
├── query.py
└── requirements.txt
```

## Files

- `chunker.py` splits markdown into heading-based chunks with breadcrumb metadata.
- `indexer.py` embeds `docs/*.md` and stores the chunks in Chroma.
- `query.py` retrieves and reranks relevant chunks.
- `ask-node.py` runs the full question-answer flow.
- `docs/` contains the local Node.js documentation corpus.
- `chroma_db/` stores the persistent vector database.

## Setup

```bash
cd labs/lab-07
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Run

Index the docs:

```bash
python3 indexer.py
```

Inspect retrieval results:

```bash
python3 query.py "How do I read a file asynchronously?"
```

Ask a full question:

```bash
python3 ask-node.py "How do I read a file in Node.js?"
```

## Notes

- `indexer.py` uses `collection.add(...)`, so re-indexing into the same database can fail on duplicate IDs.
- The answering prompt tells the model to rely only on retrieved documentation context.
