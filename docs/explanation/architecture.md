# System Architecture

The Recall System is an Advanced Recall System powered by Large Language Models and vector embeddings.

## Neuro-Symbolic Memory
We use a neuro-symbolic approach, combining:
*   **Vector Memory Store**: Semantic search using embeddings (ChromaDB, SentenceTransformers).
*   **Knowledge Graph**: Symbolic connections between entities (NetworkX).

## Signal Intelligence
`.ans` files (acting as `AGENTS.md`) in the root and subdirectories inject 'neuro-symbolic' and 'signal intelligence' context to LLMs using `<system_graph>` XML representations. This allows LLMs to reason about both semantic similarities and symbolic relationships.
