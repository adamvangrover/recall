# AGENTS.md: LLM Interaction

This document provides a guide for AI agents developing the LLM Interaction module for the Total Recall System.

## 1. Objective
To manage all communication with the Large Language Model (LLM) APIs.

## 2. Key Responsibilities

### 2.1. API Abstraction
- Create a layer of abstraction over the LLM API to simplify communication.
- This should include functions for:
    - Sending prompts to the LLM
    - Receiving and parsing responses from the LLM

### 2.2. Prompt Engineering
- Develop and maintain the prompts that are used to interact with the LLM.
- These prompts should be designed to elicit the desired responses from the LLM.

### 2.3. Error Handling
- Implement robust error handling to deal with API errors and other issues.

## 3. Guiding Principles

- **Flexibility:** The module should be designed to work with different LLM APIs.
- **Efficiency:** The module should be designed to minimize the number of API calls.
