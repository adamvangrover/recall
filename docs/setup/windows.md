# Setup Guide for Windows

To install the Recall System on Windows, follow these steps:

1.  **Clone the repository:**
    ```powershell
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

3.  **Install the package in development mode:**
    ```powershell
    pip install -e .
    ```

4.  **Vector DB Storage Management:**
    By default, the Vector DB (ChromaDB) stores data in `~\.chroma_db` (using `os.path.expanduser`). Ensure your Windows user has write access to their home directory.

5.  **Verify installation:**
    ```powershell
    recall --help
    ```