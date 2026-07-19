# Setup Guide for macOS

To install the Recall System on macOS, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the package in development mode:**
    ```bash
    pip install -e .
    ```

4.  **Vector DB Storage Management:**
    By default, the Vector DB (ChromaDB) stores data in `~/.chroma_db`. Ensure your macOS user has write access to their home directory.

5.  **Verify installation:**
    ```bash
    recall --help
    ```