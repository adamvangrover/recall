---
module: ontologies
type: core_entities
status: stable
dependencies: [docs/memory/knowledge_graph.md, docs/memory/vector_store.md]
---

# Core Entities and Ontologies

This document defines the foundational semantic structure for the Total Recall System, enabling cross-compatibility and portable natural-language translation.

## Entities
1. **Snapshot**: A distinct, immutable record of user context (e.g., UI state, extracted OCR text, application active window) at a specific timestamp.
2. **Embedding**: The mathematical, dense vector representation of a Snapshot or query, enabling semantic search.
3. **Graph Node**: The symbolic representation of a Snapshot or extracted semantic concept inside the Knowledge Graph.
4. **Edge/Relationship**: A defined semantic link between Graph Nodes (e.g., `RELATED_TO`, `CONTAINS`, `HAPPENED_BEFORE`), powered by NLP heuristics or manual linking.

## Relationships and Interoperability
- A **Snapshot** yields one or more **Embeddings**.
- A **Snapshot** is mapped to one or more **Graph Nodes**.
- The system must support converting these entities from **full binaries** (raw storage formats) into **natural language** for LLM interpretation or human review.
