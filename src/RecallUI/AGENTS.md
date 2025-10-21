# AGENTS.md: Recall Interface (Phase 3)

This document provides a guide for AI agents developing the Recall Interface for the Total Recall System.

## 1. Objective
Build the user-facing application for searching and interacting with the recall history.

## 2. Key Requirements

### 2.1. Timeline Interface
- Replace the simple log view with a rich, interactive timeline.
- Allow users to scroll visually through their history.

### 2.2. Semantic Search
- The search bar will accept natural language queries.
- The query will be converted to a vector embedding using the same local model as the Retrieval Core.
- The result will be a similarity search against the local vector database.

### 2.3. Actionable Snapshots ("Click to Do")
- When a user selects a snapshot from the timeline, the interface must allow them to:
    - Select and copy text directly from the snapshot image (using the stored OCR data).
    - Select, crop, and save images or portions of the snapshot.

### 2.4. UI/UX
- The interface must be intuitive, fast, and clearly communicate the system's status (e.g., capturing, paused).

## 3. Deliverable
A standalone desktop application that allows users to search and interact with their captured history.
