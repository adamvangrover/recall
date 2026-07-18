---
type: system_architecture
project: Total Recall System
stack:
  - python
  - chromadb
  - networkx
  - click
  - pytest
architecture_pattern: modular neuro-symbolic memory
security: zero-trust hardware-anchored
processing: local on-device
status: stable
---

# Core Directives

This document defines the symbolic foundation, immutable laws, tech stack, and design patterns for the Total Recall System.

## Architectural Expansion
- **Ontologies**: The system defines core entities and semantic relationships to map complex contexts into simple, portable nodes.
- **Data Layers & Connectors**: Storage is abstracted to ensure compatibility with various binary formats (Vector, Graph), connected via modular adapters.
- **State Management**: Fluid transition between raw binary state and Natural Language representations based on agent or user preference, with rigorous token budgeting.

## Critical Invariants (DO NOT BREAK)

- **User Sovereignty**: The user has absolute and sole control over their data. The system is a personal tool, not a data collection service.
- **Privacy & Security by Design**: The architecture MUST be built on a zero-trust, hardware-anchored security model.
- **On-Device Processing**: All user data (snapshots, OCR text, embeddings) MUST be processed and stored locally on the user's machine. No personal data is sent to the cloud for AI processing.
- **Seamless Integration**: The system must operate efficiently in the background, leveraging NPUs to avoid performance degradation.
- **File System Memory**: Use the neuro-symbolic markdown memory system (`@` files and `docs/memory/`) for storing architecture states, active contexts, and decision histories.
- **Interoperability**: The architecture must support translation from full binaries to natural language to accommodate user, reviewer, or agent token and state management needs.
