---
module: knowledge_graph
type: symbolic_node
dependencies: [networkx]
status: stable
---

## Semantic Core
Maintains relational knowledge between memory items to create an advanced recall system. This allows finding related concepts and context-aware retrieval.
Implemented in `KnowledgeGraph` using the `networkx` library.

## Critical Invariants (DO NOT BREAK)
- The graph structure must be serialized securely to JSON.
- Contextual ranking is determined by similarity, recency, and frequency (via `ContextManager`).
- Auto-tagging and summarization rely on heuristic models (via `NLPUtils`).

## Recent Memory Signals
- Initialized core capabilities using NetworkX for relational storage.
