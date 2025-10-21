# AGENTS.md: Command-Line Interface (CLI)

This document provides a guide for AI agents developing the Command-Line Interface (CLI) for the Total Recall System.

## 1. Objective
To provide a user-friendly and intuitive command-line interface for interacting with the Total Recall System.

## 2. Key Responsibilities

### 2.1. Command Handling
- Implement the main commands for the application, such as:
    - `recall add "memory"`: Adds a new memory to the system.
    - `recall search "query"`: Searches for memories based on a query.
    - `recall list`: Lists all memories.
    - `recall delete <id>`: Deletes a memory by its ID.
- Use a library like `click` or `argparse` to handle command-line arguments and options.

### 2.2. User Interaction
- Provide clear and concise feedback to the user.
- Handle user input and errors gracefully.

## 3. Guiding Principles

- **Usability:** The CLI should be easy to use and understand.
- **Consistency:** The commands and options should follow a consistent naming convention.
