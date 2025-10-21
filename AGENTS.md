# AGENTS.md: Total Recall System (Portable LLM Edition)

This document provides a comprehensive guide for AI agents involved in the development of the Total Recall System. It outlines the project's vision, core principles, and architecture for a portable, LLM-powered application.

## 1. Project Vision & Goals

### 1.1. Vision
To create a portable, secure, and powerful personal recall system that provides users with a searchable, semantic memory of their digital interactions, powered by Large Language Models (LLMs). The system will be accessible via a command-line interface (CLI) and potentially on mobile devices.

### 1.2. Core Principles
- **Portability:** The system should be able to run on any platform that supports Python.
- **LLM-Native:** The system will leverage the power of LLMs for its core functionality, including memory storage, retrieval, and analysis.
- **User Control:** The user has control over their data and can manage their memories through the CLI.
- **Security:** The user's API keys and other sensitive data must be handled securely.

## 2. Architectural Overview

The system is designed as a Python-based command-line application with a modular architecture.

- **Core Logic (`src/core`):** Contains the main business logic and data models for the application.
- **Command-Line Interface (`src/cli`):** Provides the user interface for interacting with the system.
- **LLM Interaction (`src/llm`):** Manages all communication with the LLM APIs.
- **Security (`src/security`):** Handles the secure storage and management of API keys and other sensitive data.

## 3. Development Guidelines

- **Modularity:** Each component should be developed as a self-contained module with a well-defined API.
- **Testability:** The code should be written in a way that allows it to be easily tested.
- **Dependency Management:** All dependencies should be managed in the `requirements.txt` file.
