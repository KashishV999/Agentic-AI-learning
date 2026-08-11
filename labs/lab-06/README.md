# Lab 06: Semantic Product Search

## Why This Lab Exists

This lab is for learning embeddings and semantic retrieval. Instead of keyword matching, the project turns product records into vectors so a search query can find meaning-based matches, then improve the ranking with a second relevance pass.

## What I Learned On The First Pass

- How to serialize structured product data into text before embedding it.
- Why embeddings let me search by meaning instead of exact words.
- How vector similarity works in a small local search system.
- Why reranking helps after the first retrieval step.
- How to store vectors and metadata on disk for a simple search pipeline.

## Core AI And Tech Topics

- Embeddings
- Semantic search
- Vector indexing
- Cosine similarity
- Reranking
- Retrieval pipelines

## Folder Structure

```text
lab-06/
├── README.md
├── indexer.py
├── metadata.tsv
├── products.json
├── requirements.txt
├── screenshots/
│   └── cluster.png
├── search.py
├── temp_script.py
├── utils.py
└── vectors.tsv
```

## Files

- `indexer.py` fetches product data, serializes items, generates embeddings, and writes output files.
- `utils.py` contains serialization, similarity, reranking, and data-loading helpers.
- `search.py` is the interactive CLI for product search.
- `temp_script.py` is a small threshold experiment.
- `products.json`, `vectors.tsv`, and `metadata.tsv` are generated data files.
- `screenshots/cluster.png` is a saved visualization asset.

## Setup

```bash
cd labs/lab-06
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Run

Build the local index:

```bash
python3 indexer.py
```

Search interactively:

```bash
python3 search.py
```

Optional:

```bash
python3 temp_script.py
```

## Notes

- `indexer.py` appends to `vectors.tsv`, so a clean rebuild may require deleting old generated files first.
- Product data is fetched from DummyJSON.
