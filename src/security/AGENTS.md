# AGENTS.md: Security

This document provides a guide for AI agents developing the Security module for the Total Recall System.

## 1. Objective
To handle the secure storage and management of API keys and other sensitive data.

## 2. Key Responsibilities

### 2.1. API Key Management
- Securely store and retrieve API keys for LLM services.
- Use a library like `keyring` to store keys in the system's keychain.
- Provide a command-line interface for adding and removing API keys.

### 2.2. Data Encryption
- Implement encryption for any sensitive data that is stored locally.
- Use a strong encryption algorithm like AES-256.

## 3. Guiding Principles

- **Principle of Least Privilege:** The module should only have access to the data that it needs to perform its functions.
- **Secure by Default:** The module should be secure by default and should not require any special configuration to be secure.
