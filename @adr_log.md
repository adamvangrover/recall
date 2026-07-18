---
type: decision_ledger
project: Total Recall System
---

# Architecture Decision Records (ADR)

This file maintains the contextual history of critical architectural choices to prevent context collapse and regressions.

## ADR-001: Modular Neuro-Symbolic Memory File System

**Date:** 2024-05-18

**Context:**
Autonomous "adversarial" coding agents often suffer from context collapse over long timelines when a single monolithic context file is used (e.g., `AGENTS.md` or `.cursorrules`). The LLM forgets why a piece of code was written and may attempt to change it, re-introducing bugs, and generating noise when processing the context.

**Decision:**
We adopted a modular neuro-symbolic memory layer where memory is broken down into a strictly enforced, semantic hierarchy:
1. `@system_architecture.md`: The symbolic foundation and immutable laws.
2. `@current_context.md`: The active state or short-term working memory.
3. `docs/memory/`: The knowledge graph of semantic nodes.
4. `@adr_log.md`: The decision ledger or contextual history.
These markdown files will act as an API that the LLM agent can query and mutate (read/write loop) to persistently document the architecture.

**Consequences:**
- The LLM agent requires explicit instructions or tooling to systematically update these state files when resolving bugs, changing architecture, or completing objectives.
- Old context mechanisms (like large monolithic `AGENTS.md` files) might need to be deprecated or refactored into this new structure.
- Reduces hallucination rates and allows massive modular scale.

## ADR-002: Modular Expansion of Memory Primitives

**Date:** 2024-05-18

**Context:**
To achieve the long-term goal of the Recall system, the architecture must support robust compatibility with multiple data layers, seamless transition between raw binary states and natural language, and rigorous token state management.

**Decision:**
Expanded the memory layer by introducing specific ontologies, data layer abstractions, modular connectors, and state management rules. The file structure within `docs/memory/` now acts as an extensible graph encompassing:
- Ontologies (Core Entities and semantics)
- Data Layers (Storage abstraction and NL translation)
- Connectors (Specific DB implementations like ChromaDB)
- State Management (Token lifecycle and representation switching)

**Consequences:**
- Further compartmentalizes architectural rules, requiring agents to traverse subdirectories for specific contexts.
- Enables more precise injection of rules related to data storage format and token budgeting.
