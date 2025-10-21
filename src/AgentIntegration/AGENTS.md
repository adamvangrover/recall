# AGENTS.md: Advanced Applications & Agentic Integration (Phase 5)

This document provides a guide for AI agents developing the Advanced Applications & Agentic Integration for the Total Recall System.

## 1. Objective
Extend the system's capabilities from a passive log to a proactive agentic memory layer.

## 2. Key Requirements

### 2.1. Contextual Layer (PKG Proof-of-Concept)
- Develop an on-device entity and relationship extraction model.
- Run this model over the recall data to populate a local Personal Knowledge Graph (PKG), connecting entities like people, projects, and documents.

### 2.2. Agent API
- Design and build a secure, local-only API.
- This API will allow trusted, user-permissioned AI agents (e.g., "Adam") to query the recall log and PKG for long-term memory and context.
- Access must be strictly controlled by the user.

### 2.3. Explainable AI (XAI) Output
- For features like automated meeting summarization, the AI model must be designed to provide a "SHAP-like rationale."
- For each conclusion in a generated summary, the system must cite and display the specific text snippets or snapshot images from the recall log that were the primary drivers for that conclusion.

## 3. Deliverable
An extended system with a queryable API for AI agents and demonstrable explainability features.
