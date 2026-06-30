# CLAUDE.md: Memory System

This document provides a guide for AI agents developing the Memory module for the Total Recall System.

## 1. Objective
To manage hybrid neuro-symbolic storage, including semantic vectors, contextual ranking, and knowledge graphs.

## 2. Key Responsibilities
- Manage `VectorMemoryStore` (ChromaDB + Sentence Transformers) for semantic embeddings.
- Maintain `KnowledgeGraph` using NetworkX for symbolic, relational representation.
- Apply `NLPUtils` for heuristic tagging, and `ContextManager` for contextual relevance ranking.
- Optimize storage usage using `MemoryOptimizer`.

## 3. Neuro-Symbolic System Architecture (Signal Intelligence)

<system_graph>
  <entities>
    <entity id="VectorMemoryStore" type="Neural_Storage" />
    <entity id="KnowledgeGraph" type="Symbolic_Storage" />
    <entity id="ContextManager" type="Ranking_Engine" />
  </entities>
  <relationships>
    <relationship source="VectorMemoryStore" target="KnowledgeGraph" type="coupled_retrieval" />
    <relationship source="ContextManager" target="VectorMemoryStore" type="ranks_results" />
  </relationships>
  <signal_flows>
    <flow id="Hybrid_Memory_Recall">
      <step>Query is embedded and matched in VectorMemoryStore.</step>
      <step>Linked entities are traversed in KnowledgeGraph.</step>
      <step>ContextManager re-ranks combined signals for highest semantic significance.</step>
    </flow>
  </signal_flows>
</system_graph>

## 4. Guiding Principles
- **Dual Representation:** Always synchronize neural and symbolic stores when meaningful relationships are detected.
- **Performance:** Bulk updates should be used for access counts to avoid N+1 bottlenecks.
