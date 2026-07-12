# Lab 7: RAG (Retrieval Augmented Generation)

## Introduction
Build a RAG system that answers questions about Node.js documentation by retrieving relevant sections, reranking them for accuracy, and feeding them to an LLM for synthesis. This lab demonstrates how to combine semantic search with LLM-powered responses.

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set `OPENROUTER_API_KEY` in a `.env` file.
3. Index the documentation:
   ```bash
   python indexer.py
   ```
4. Ask a question:
   ```bash
   python ask-node.py "How do I read a file in Node.js?"
   ```

## Files
- `chunker.py` - Splits markdown files by headings, removes HTML comments, and creates searchable chunks with breadcrumb metadata.
- `indexer.py` - Reads all markdown docs, chunks them, embeds via OpenAI, and persists to Chroma vector database.
- `query.py` - Searches the Chroma DB for relevant chunks, reranks results with Cohere, and formats them for LLM context.
- `ask-node.py` - CLI tool that takes a user question, searches the indexed docs, and generates an answer using Gemini with the retrieved context.
- `docs/` - Node.js official documentation markdown files (source material for indexing).
- `chroma_db/` - Persistent vector database storing embeddings and chunk metadata.

## Basics
- **Chroma:** Vector database that stores embeddings and enables similarity search.
- **Pipeline:** Chunk → Embed → Store → Search → Rerank → LLM Answer.
- **Reranking:** Cohere's cross-encoder improves relevance ordering before LLM synthesis.
- **Context Grounding:** LLM only answers from provided docs; prevents hallucination.


## Visualizing Embeddings

chroma browse shows fails to load error, so ran this in `DB Browser for sqlite` by opening the `chroma_db/chroma.sqlite` file 
```sql
SELECT 
    e.id AS chunk_id,
    fts.c0 AS document,
    MAX(CASE WHEN em.key = 'source' THEN em.string_value END) AS source,
    MAX(CASE WHEN em.key = 'heading' THEN em.string_value END) AS heading,
    MAX(CASE WHEN em.key = 'breadcrumb' THEN em.string_value END) AS breadcrumb
FROM embeddings e
LEFT JOIN embedding_metadata em ON em.id = e.id
LEFT JOIN embedding_fulltext_search_content fts ON fts.id = e.id
GROUP BY e.id

```