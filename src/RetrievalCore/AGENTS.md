# AGENTS.md: Retrieval Core (Phase 2)

This document provides a guide for AI agents developing the Retrieval Core for the Total Recall System.

## 1. Objective
Implement the on-device AI pipeline to process snapshots and enable semantic search.

## 2. Key Requirements

### 2.1. Hardware Prerequisite
- The system must detect and require a Neural Processing Unit (NPU) with a minimum of 40 TOPS.
- The system should gracefully disable itself if the hardware requirement is not met.

### 2.2. Local AI Models
- Integrate a lightweight, on-device OCR model to extract all text from each snapshot.
- Integrate a state-of-the-art, multimodal embedding model (e.g., a variant of SigLIP or CLIP, optimized for ONNX Runtime) to convert the image and its extracted text into a single vector embedding.
- This entire process must run locally, accelerated by the NPU.

### 2.3. Vector Database
- Integrate a lightweight, in-process vector database (e.g., LanceDB, ChromaDB) to store and index the embeddings generated from each snapshot.
- The database must be stored locally within the encrypted data folder.

### 2.4. Indexing Pipeline
- Develop the workflow that orchestrates the process for each new snapshot: Capture -> OCR -> Generate Embedding -> Index in Vector DB.

## 3. Deliverable
An automated pipeline that processes captured snapshots into a searchable, local semantic index.
