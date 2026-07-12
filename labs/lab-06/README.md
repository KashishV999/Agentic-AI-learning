# Lab 6: Semantic Search & Vector Spaces

A  Python lab for building a semantic product search engine using embeddings and reranking.

## What this is for
- Serialize product data into compact text.
- Build a vector index with OpenAI embeddings.
- Visualize embeddings in TensorFlow Embedding Projector.
- Search with cosine similarity and rerank results for better relevance.

## Usage
1. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Add `OPENROUTER_API_KEY` to a `.env` file.
3. Generate the index:
   ```bash
   python indexer.py
   ```
4. Run the interactive search CLI:
   ```bash
   python search.py
   ```
5. Optional: inspect threshold behavior:
   ```bash
   python temp_script.py
   ```

## Files
- `indexer.py` - Fetches product data, serializes each product, creates embeddings, and writes `products.json`, `vectors.tsv`, and `metadata.tsv`.
- `utils.py` - Contains serialization, dot-product similarity, database loading, search logic, and reranking via OpenRouter.
- `search.py` - Interactive command-line search interface that prints rerank and vector scores for results.
- `temp_script.py` - Quick threshold experiment script for comparing good vs bad query similarity scores.
- `products.json` - Saved raw product catalog from DummyJSON.
- `vectors.tsv` - Precomputed embedding vectors for search.
- `metadata.tsv` - TSV metadata for embedding visualization.
