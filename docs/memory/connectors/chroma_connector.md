---
module: connectors
type: vector_db_adapter
status: stable
dependencies: [docs/memory/data_layers/storage_abstraction.md, docs/memory/vector_store.md]
---

# ChromaDB Connector

This document defines the specific implementation requirements for connecting the Total Recall System to ChromaDB.

## Connector Specifications
- **Provider**: ChromaDB (Local/On-device)
- **Role**: Serves as the primary vector storage engine for Snapshots and semantic memories.
- **Interoperability**: Must conform to the `IRecallStorage` primitive defined in the storage abstraction layer.

## Invariants
- Connection must be isolated and strictly adhere to local processing (no cloud telemetry).
- Must handle bulk upserts to maintain performance limits.
- Supports translating vector similarity results directly into Natural Language contexts via the `NLTranslator`.
