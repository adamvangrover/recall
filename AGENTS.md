# AGENTS.md: Total Recall System

This document provides a comprehensive guide for AI agents involved in the development of the Total Recall System. It outlines the project's vision, core principles, architecture, and phased implementation plan.

## 1. Project Vision & Goals

### 1.1. Vision
To create a secure, private, and powerful personal recall system that provides users with a searchable, semantic memory of their digital interactions. The system will act as a foundational layer for augmenting human intelligence and enabling proactive, agentic AI workflows.

### 1.2. Core Principles
- **User Sovereignty:** The user has absolute and sole control over their data.
- **Privacy & Security by Design:** The architecture is built on a zero-trust, hardware-anchored security model.
- **On-Device Processing:** All user data is processed and stored locally on the user's machine.
- **Seamless Integration:** The system operates efficiently in the background without performance degradation.

### 1.3. Foundational Document
All development must adhere to the principles and findings outlined in the research paper: "The Total Recall System: Architecture, Applications, and Strategic Implications of Comprehensive Personal Data Logging."

## 2. Architectural Overview

The system is composed of several key components, each with a specific responsibility. The architecture is designed to be modular, with each component developed and maintained independently.

- **Ingestion Engine:** A background service for securely capturing and storing screen snapshots.
- **Retrieval Core:** An on-device AI pipeline for processing snapshots and enabling semantic search.
- **Recall Interface:** A user-facing application for searching and interacting with the recall history.
- **Security & Privacy:** A framework for ensuring the security and privacy of user data.
- **Agentic Integration:** An API for allowing trusted AI agents to access the recall log.

## 3. Phased Implementation Plan

The project is divided into five phases. Each phase has a specific set of objectives and deliverables.

- **Phase 1: The Ingestion Engine:** Develop the background service for capturing and storing screen snapshots.
- **Phase 2: On-Device Intelligence:** Implement the on-device AI pipeline for processing snapshots and enabling semantic search.
- **Phase 3: The User Experience:** Build the user-facing application for searching and interacting with the recall history.
- **Phase 4: Security & Privacy Hardening:** Re-architect the system to meet the zero-trust security and privacy requirements.
- **Phase 5: Advanced Applications & Agentic Integration:** Extend the system's capabilities to a proactive agentic memory layer.

## 4. Development Guidelines

- **Modularity:** Each component should be developed as a self-contained module with a well-defined API.
- **Portability:** The code should be written in a way that allows it to be easily ported to other platforms.
- **Self-Contained Prompts:** Each component's `AGENTS.md` file should contain all the information necessary for an AI agent to develop that component.
