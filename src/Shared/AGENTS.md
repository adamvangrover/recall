# AGENTS.md: Shared Components

This document provides a guide for AI agents developing the Shared Components for the Total Recall System.

## 1. Objective
To create a central repository of shared code, utilities, and data structures that can be used by all other components of the Total Recall System.

## 2. Key Responsibilities

### 2.1. Data Models
- Define and maintain the core data models for the system, such as the `Snapshot` and `Metadata` objects.
- Ensure that these models are serializable and can be easily stored and retrieved from the database.

### 2.2. Utilities
- Develop and maintain a set of utility classes and functions for common tasks, such as:
    - File I/O
    - Database access
    - Error handling and logging
    - Configuration management

### 2.3. Constants and Enums
- Define and maintain a set of constants and enums that are used throughout the application.

## 3. Guiding Principles

- **Reusability:** The code in this component should be designed to be as reusable as possible.
- **Stability:** The code in this component should be well-tested and stable.
- **Dependency Management:** The Shared component should have minimal dependencies on other components.
