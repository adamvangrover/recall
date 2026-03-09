import uuid
import os
import chromadb
import datetime
import zlib
from src.core.embedding import EmbeddingService
from src.memory.nlp_utils import NLPUtils

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

        # Auto-Intelligence via NLPUtils
        nlp_data = NLPUtils.auto_process(content)
        metadata['tags'] = ",".join(nlp_data['tags'])
        metadata['summary'] = nlp_data['summary']

        # Storage Compression Tracking (Simulated via zlib)
        original_size = len(content.encode('utf-8'))
        compressed_size = len(zlib.compress(content.encode('utf-8')))
        compression_ratio = compressed_size / original_size if original_size > 0 else 1.0

        metadata['original_size'] = original_size
        metadata['compressed_size'] = compressed_size
        metadata['compression_ratio'] = compression_ratio

        # Usage Tracking
        metadata['creation_date'] = datetime.datetime.now().isoformat()
        metadata['last_accessed'] = datetime.datetime.now().isoformat()
        metadata['access_count'] = 1

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
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        if not results or not results.get('ids'):
            return []

        ids = results['ids'][0]
        documents = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]

        memories = []
        update_ids = []
        update_metas = []

        for id, doc, dist, meta in zip(ids, documents, distances, metadatas):
            # Track access for bulk update
            meta['access_count'] = meta.get('access_count', 0) + 1
            meta['last_accessed'] = datetime.datetime.now().isoformat()
            update_ids.append(id)
            update_metas.append(meta)

            memories.append({
                "id": id,
                "content": doc,
                "similarity": 1 - dist,
                "metadata": meta
            })

        # Bulk update access stats
        if update_ids:
            self._collection.update(
                ids=update_ids,
                metadatas=update_metas
            )

        return memories

    def get_memory(self, memory_id: str) -> dict:
        """
        Retrieves a single memory by ID and updates access stats.
        """
        results = self._collection.get(ids=[memory_id])
        if not results or not results.get('ids'):
            return None

        doc = results['documents'][0]
        meta = results['metadatas'][0]

        self._update_access_stats(memory_id, meta)

        return {
            "id": memory_id,
            "content": doc,
            "metadata": meta
        }

    def _update_access_stats(self, memory_id: str, meta: dict):
        """
        Updates the access count and last accessed time.
        """
        meta['access_count'] = meta.get('access_count', 0) + 1
        meta['last_accessed'] = datetime.datetime.now().isoformat()
        self._collection.update(
            ids=[memory_id],
            metadatas=[meta]
        )

    def list_memories(self, include_metadata: bool = False) -> list[dict]:
        """
        Lists all memories in the store.
        """
        includes = ['documents', 'metadatas'] if include_metadata else ['documents']
        results = self._collection.get(include=includes)
        if not results or not results.get('ids'):
            return []

        memories = []
        for i, memory_id in enumerate(results['ids']):
            memory = {"id": memory_id, "content": results['documents'][i]}
            if include_metadata and results.get('metadatas'):
                memory["metadata"] = results['metadatas'][i]
            memories.append(memory)

        return memories

    def delete_memory(self, memory_id: str) -> bool:
        """
        Deletes a memory by its ID.
        """
        self._collection.delete(ids=[memory_id])
        return True
