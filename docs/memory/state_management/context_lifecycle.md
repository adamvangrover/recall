---
module: state_management
type: token_and_state_lifecycle
status: draft
dependencies: [docs/memory/ontologies/core_entities.md]
---

# Context Lifecycle & Token Management

This document governs how the system handles the transition of data states and the management of LLM context windows (tokens).

## Token Management Strategy
- **Budgeting**: The system must enforce a strict token budget for LLM contexts to prevent context collapse.
- **Compression**: Cold memories and expansive graph neighborhoods must be summarized or compressed into denser natural language representations when approaching token limits.
- **Dynamic Loading**: Context is paged in and out of the active prompt dynamically based on the current objective.

## State Transitions (Binary <-> Natural Language)
- The architecture supports fluid transitions based on preference (Human, Agent, Model).
- **Binary State**: Highly efficient, dense storage (ChromaDB binaries, NetworkX JSON) used for long-term persistence and exact retrieval.
- **Natural Language State**: Unpacked, verbose text representations of the binary data, optimized for LLM comprehension, logical reasoning, and human review.
- The system manages these states via the `NLTranslator` to seamlessly project binaries into the token space without losing semantic intent.
