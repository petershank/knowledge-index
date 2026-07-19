# Knowledge Index

A lightweight, high-performance personal "Second Brain" pipeline. It aggregates, normalizes, and indexes local files into a single, lightning-fast searchable knowledge base.

## Features

- **Blazing Fast Ingestion**: Scans thousands of repository files and indexes them in under 2 seconds.
- **Recursive Directory Pruning**: High-performance crawler skips unneeded dependency trees (`node_modules`, `venv`) at the root.
- **Deterministic Identity**: Generates unique, stable SHA-256 path hashes to ensure strict idempotency and zero duplicate entries.
- **SQLite FTS5 Search**: Uses a dual-table relational and virtual search schema for instant, ranked full-text keyword matching with dynamic text snippets.

## Architecture

```text
       Sources (Git repos)
                |
     Recursive Ingest Filter (os.walk / Pruning)
                |
      Document Normalization (Path Hashing)
                |
         SQLite Engine
        /             \
  [documents]     [documents_fts]
  (Metadata)      (Virtual Full-Text Search)
```

## Usage

### Indexing Files

To scan and index configured repositories into `knowledge.db`:

```bash
python -m knowledge.index
```

### Searching the Index

To query your knowledge base from the terminal:

```bash
python -m knowledge.search "your_search_term"
```

---

## Next Milestones

- 📝 **macOS Notes.app Integration**: Build a native extractor to parse your local Apple Notes database files and merge your frictionless notes into this unified index.
- 🔍 **Advanced FTS5 Queries**: Upgrade the search utility to support wildcards (e.g., `fac*` matches `factors`), prefix matching, and complex Boolean logic (`prime AND practice`).
- 🏷️ **Schema Refinement & Language Tags**: Extend the metadata table to capture code languages, file extensions, or tags for precise query filtering.
- 🤖 **Semantic Vector Embeddings**: Integrate a local embedding model to unlock meaning-based semantic search alongside your keyword matching.
