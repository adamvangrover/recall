import uuid
import os
import chromadb
import datetime
from src.core.embedding import EmbeddingService

class VectorMemoryStore:
    def __init__(self, path="~/.recall_vectordb"):
        self._client = chromadb.PersistentClient(path=os.path.expanduser(path))
        self._collection = self._client.get_or_create_collection(name="memories")
        self._embedding_service = EmbeddingService()

    def add_memory(self, content: str, metadata: dict = None) -> str:
        """
        Adds a new memory to the vector store.
        """
        memory_id = str(uuid.uuid4())
        embedding = self._embedding_service.generate_embedding(content)

        if metadata is None:
            metadata = {}

        metadata['creation_date'] = datetime.datetime.now().isoformat()

        self._collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id

    def search_memory(self, query: str, n_results: int = 5) -> list[dict]:
        """
        Performs a semantic search for memories similar to the query.
        """
        query_embedding = self._embedding_service.generate_embedding(query)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        if not results or not results.get('ids'):
            return []

        ids = results['ids'][0]
        documents = results['documents'][0]
        distances = results['distances'][0]

        return [
            {"id": id, "content": doc, "similarity": 1 - dist}
            for id, doc, dist in zip(ids, documents, distances)
        ]

    def list_memories(self) -> list[dict]:
        """
        Lists all memories in the store.
        """
        results = self._collection.get()
        return [
            {"id": id, "content": doc}
            for id, doc in zip(results['ids'], results['documents'])
        ]

    def delete_memory(self, memory_id: str) -> bool:
        """
        Deletes a memory by its ID.
        """
        self._collection.delete(ids=[memory_id])
        return True
