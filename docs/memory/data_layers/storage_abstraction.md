---
module: data_layers
type: storage_abstraction
status: active
dependencies: [docs/memory/ontologies/core_entities.md]
---

# Storage Abstraction Layer

This document outlines the primitives required for full data layer compatibility within the Total Recall System.

## Principles of Data Portability
- **Agnostic Storage**: The core logic must abstract away the underlying database technology (e.g., SQLite, ChromaDB, NetworkX JSON).
- **Format Translation**: The storage layer must provide interfaces to serialize and deserialize data across various formats (JSON, Binary, Parquet).
- **Semantic Translation**: A core requirement is the ability to project storage state into Natural Language (NL) based on user or agent preference, seamlessly transitioning between raw DB queries and conversational DB interactions.

## Primitives
- `IRecallStorage`: Interface defining generic `insert`, `retrieve`, `update`, and `delete` operations.
- `NLTranslator`: Service responsible for mapping raw storage schemas (like graph edges or vector metadata) into human/LLM-readable text.
