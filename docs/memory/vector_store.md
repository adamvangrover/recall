---
module: vector_store
type: symbolic_node
dependencies: [chromadb, sentence-transformers, zlib-ng]
status: stable
---

## Semantic Core
Handles the underlying storage and retrieval of vector embeddings for the personal recall system.
The `VectorMemoryStore` interacts with `chromadb` to persist embeddings and uses `sentence-transformers` for encoding memory text.

## Critical Invariants (DO NOT BREAK)
- The VectorMemoryStore must resolve the persistence path using `os.path.expanduser` to prevent directory creation errors.
- Ensure metadata updates use bulk processes to avoid N+1 query performance issues when updating `access_count` or `last_accessed` metrics.
- Keep track of compression sizes mimicking zlib behaviour for optimizations.

## Recent Memory Signals
- Addressed cold memory archival features by identifying memories unused for N days (via `MemoryOptimizer`).
