# Total Recall System: Production Specification (v1.0)

## 1. Project Vision & Goals

### 1.1. Vision
To create a secure, private, and powerful personal recall system that provides users with a searchable, semantic memory of their digital interactions. The system will act as a foundational layer for augmenting human intelligence and enabling proactive, agentic AI workflows.

### 1.2. Core Principles
- **User Sovereignty:** The user has absolute and sole control over their data. The system is a personal tool, not a data collection service.
- **Privacy & Security by Design:** The architecture must be built on a zero-trust, hardware-anchored security model from the ground up.
- **On-Device Processing:** All user data, especially screen snapshots and their derivatives, must be processed and stored locally on the user's machine. No personal data is sent to the cloud for AI processing.
- **Seamless Integration:** The system should operate efficiently in the background, augmenting the user's workflow without performance degradation.

### 1.3. Foundational Document
The design, architecture, and implementation of this system must adhere to the principles and findings outlined in the research paper: "The Total Recall System: Architecture, Applications, and Strategic Implications of Comprehensive Personal Data Logging."

## 2. Architectural Evolution: From Prototype to Production

The current prototype (Personal Recall AI) validates the user experience of AI-driven log analysis but relies on manual text input and a cloud-based AI model. The production system requires a fundamental architectural shift to a fully on-device, automated system.

| Component | Prototype Implementation (Cloud-Based) | Production Architecture (On-Device) |
|---|---|---|
| Data Ingestion | Manual Text Input | Automated, secure screen capture service (Windows Service) |
| Data Storage | Firebase Firestore (Cloud) | Encrypted local SQLite database + file system for snapshots |
| AI Processing | Google Gemini API (Cloud) | Local, NPU-accelerated multimodal embedding models |
| Retrieval Core | Semantic analysis via API call | On-device Vector Database |
| Security Model | Standard web app security | Zero-Trust: Hardware-anchored, VBS isolation, E2E encryption |
| Authentication | Firebase Auth (User login) | Windows Hello ESS (Biometric proof-of-presence) |

## 3. Phased Implementation Plan

### Phase 1: The Ingestion Engine (Core Service)
- **Objective:** Develop the background service responsible for securely capturing and storing screen snapshots.
- **Key Requirements:**
    - **Windows Service:** The ingestion engine will be built as a background Windows Service that starts on user login.
    - **Secure Screen Capture:**
        - Integrate with the `Windows.Graphics.Capture` API. This is mandatory to leverage its security features (permission prompts, visual indicators, DRM protection).
        - Implement the snapshot logic: capture the active screen every ~3-5 seconds, triggered by significant on-screen changes (e.g., window focus change, new text).
    - **Data Storage:**
        - All data must be stored within a dedicated, protected folder in the user's local `AppData` directory.
        - Snapshots: Raw snapshot images (e.g., PNGs) will be stored directly on the file system within the protected folder.
        - Metadata: An SQLite database will be used to store metadata for each snapshot, including timestamp, active application name, and window title.
    - **Initial Encryption:** Implement initial file-system level encryption for the entire data store using Windows Data Protection API (DPAPI) as a baseline. This will be enhanced in Phase 4.
- **Deliverable:** A functional background service that captures and saves screen snapshots locally.

### Phase 2: On-Device Intelligence (The Retrieval Core)
- **Objective:** Implement the on-device AI pipeline to process snapshots and enable semantic search.
- **Key Requirements:**
    - **Hardware Prerequisite:** The system must detect and require a Neural Processing Unit (NPU) with a minimum of 40 TOPS. The system should gracefully disable itself if the hardware requirement is not met.
    - **Local AI Models:**
        - Integrate a lightweight, on-device OCR model to extract all text from each snapshot.
        - Integrate a state-of-the-art, multimodal embedding model (e.g., a variant of SigLIP or CLIP, optimized for ONNX Runtime) to convert the image and its extracted text into a single vector embedding. This entire process must run locally, accelerated by the NPU.
    - **Vector Database:**
        - Integrate a lightweight, in-process vector database (e.g., LanceDB, ChromaDB) to store and index the embeddings generated from each snapshot.
        - The database must be stored locally within the encrypted data folder.
    - **Indexing Pipeline:** Develop the workflow that orchestrates the process for each new snapshot: Capture -> OCR -> Generate Embedding -> Index in Vector DB.
- **Deliverable:** An automated pipeline that processes captured snapshots into a searchable, local semantic index.

### Phase 3: The User Experience (Recall Interface)
- **Objective:** Build the user-facing application for searching and interacting with the recall history.
- **Key Requirements:**
    - **Timeline Interface:** Replace the simple log view with a rich, interactive timeline that allows users to scroll visually through their history.
    - **Semantic Search:** The search bar will accept natural language queries. The query will be converted to a vector embedding using the same local model, and the result will be a similarity search against the local vector database.
    - **Actionable Snapshots ("Click to Do"):** When a user selects a snapshot from the timeline, the interface must allow them to:
        - Select and copy text directly from the snapshot image (using the stored OCR data).
        - Select, crop, and save images or portions of the snapshot.
    - **UI/UX:** The interface must be intuitive, fast, and clearly communicate the system's status (e.g., capturing, paused).
- **Deliverable:** A standalone desktop application that allows users to search and interact with their captured history.

### Phase 4: Security & Privacy Hardening (The Zero-Trust Framework)
- **Objective:** Re-architect the system to meet the non-negotiable security and privacy requirements outlined in the foundational research.
- **Key Requirements:**
    - **Mandatory Opt-In:** The feature must be disabled by default. The first-run experience must provide a clear, transparent explanation and require explicit user consent to enable.
    - **Biometric Gating:**
        - Integrate with Windows Hello Enhanced Sign-in Security (ESS).
        - Enabling the feature and accessing the Recall UI must require a successful biometric (face/fingerprint) check.
    - **Hardware-Anchored Encryption:**
        - The SQLite database and all snapshots must be encrypted at rest using a robust algorithm (e.g., AES-256).
        - The master encryption keys must be generated by and protected within the system's hardware TPM or Microsoft Pluton security processor.
        - Implement "Just-in-Time" decryption, protected by the Windows Hello ESS check.
    - **Virtualization-Based Security (VBS):** The entire Recall service (ingestion, AI processing, data store) must be architecturally isolated from the main OS by running it within a VBS secure enclave. This is the most critical step to protect the data from malware, even with administrator privileges.
    - **Granular User Controls:** The UI must provide a dedicated settings area for:
        - Excluding specific applications and websites from capture.
        - Pausing/resuming capture.
        - Viewing and deleting individual snapshots or time ranges.
        - Securely deleting the entire history.
        - Configuring data lifecycle policies (e.g., storage limits, auto-delete after X days).
- **Deliverable:** A production-hardened system that aligns with the "Privacy and Security by Design" checklist.

### Phase 5: Advanced Applications & Agentic Integration
- **Objective:** Extend the system's capabilities from a passive log to a proactive agentic memory layer.
- **Key Requirements:**
    - **Contextual Layer (PKG Proof-of-Concept):**
        - Develop an on-device entity and relationship extraction model.
        - Run this model over the recall data to populate a local Personal Knowledge Graph (PKG), connecting entities like people, projects, and documents.
    - **Agent API:**
        - Design and build a secure, local-only API.
        - This API will allow trusted, user-permissioned AI agents (e.g., "Adam") to query the recall log and PKG for long-term memory and context. Access must be strictly controlled by the user.
    - **Explainable AI (XAI) Output:**
        - For features like automated meeting summarization, the AI model must be designed to provide a "SHAP-like rationale."
        - For each conclusion in a generated summary, the system must cite and display the specific text snippets or snapshot images from the recall log that were the primary drivers for that conclusion.
- **Deliverable:** An extended system with a queryable API for AI agents and demonstrable explainability features.
