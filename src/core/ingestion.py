import os
import glob
from src.memory.vector_store import VectorMemoryStore

class IngestionService:
    def __init__(self, memory_store: VectorMemoryStore):
        self.memory_store = memory_store

    def ingest_directory(self, directory_path: str) -> int:
        """
        Scans a directory for text files and adds them to memory.
        Returns the count of files ingested.
        """
        if not os.path.isdir(directory_path):
            return 0

        count = 0
        extensions = ['*.txt', '*.md']
        for ext in extensions:
            files = glob.glob(os.path.join(directory_path, ext))
            for file_path in files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        self.memory_store.add_memory(
                            content=content,
                            metadata={"source": "file", "path": file_path}
                        )
                        count += 1
        return count
