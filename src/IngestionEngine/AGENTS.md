# AGENTS.md: Ingestion Engine (Phase 1)

This document provides a guide for AI agents developing the Ingestion Engine for the Total Recall System.

## 1. Objective
Develop a background Windows Service responsible for securely capturing and storing screen snapshots.

## 2. Key Requirements

### 2.1. Windows Service
- The ingestion engine must be built as a background Windows Service.
- The service must start automatically on user login.

### 2.2. Secure Screen Capture
- Integrate with the `Windows.Graphics.Capture` API. This is mandatory to leverage its security features (permission prompts, visual indicators, DRM protection).
- Implement the snapshot logic:
    - Capture the active screen every ~3-5 seconds.
    - Trigger captures by significant on-screen changes (e.g., window focus change, new text).

### 2.3. Data Storage
- All data must be stored within a dedicated, protected folder in the user's local `AppData` directory.
- Snapshots: Raw snapshot images (e.g., PNGs) will be stored directly on the file system within the protected folder.
- Metadata: An SQLite database will be used to store metadata for each snapshot, including:
    - Timestamp
    - Active application name
    - Window title

### 2.4. Initial Encryption
- Implement initial file-system level encryption for the entire data store using the Windows Data Protection API (DPAPI) as a baseline.

## 3. Deliverable
A functional background service that captures and saves screen snapshots locally.
