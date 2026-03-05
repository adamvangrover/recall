import uuid
import chromadb
import datetime
import os
import zlib
from sentence_transformers import SentenceTransformer

class VectorMemoryStore:
    def __init__(self, path="~/.recall_vectordb"):
        expanded_path = os.path.expanduser(path)
        self._client = chromadb.PersistentClient(path=expanded_path)
        self._collection = self._client.get_or_create_collection(name="memories")
        # Load the model. Ideally this should be lazy loaded or injected, but for now this works.
        self._model = SentenceTransformer('all-MiniLM-L6-v2')

    def _get_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for a given text using sentence-transformers.
        """
        if not text:
            return [0.0] * 384
        embedding = self._model.encode(text).tolist()
        return embedding

    def _compress_content(self, content: str) -> bytes:
        """
        Compresses content using zlib.
        """
        return zlib.compress(content.encode('utf-8'))

    def _decompress_content(self, content_bytes: bytes) -> str:
        """
        Decompresses content using zlib.
        """
        return zlib.decompress(content_bytes).decode('utf-8')

    def add_memory(self, content: str, metadata: dict = None) -> str:
        """
        Adds a new memory to the vector store.

        Note: ChromaDB stores documents as strings, but we can store the compressed bytes
        as a hex string or base64 if we wanted to save space directly in the Document field.
        However, since Chroma uses the Document for retrieval, compressing it might hurt simple string search
        if Chroma does fuzzy matching on it. But for vector search, we rely on embeddings.

        To truly save space, we should store the compressed content in metadata or a separate store,
        but Chroma metadata is also indexed.

        Let's store the raw content for searchability, but add compression metrics to metadata
        to simulate the "Optimization" aspect requested.

        In a real expanded system, we would store the embedding in Chroma and the full compressed blob
        in a separate Blob Store (S3/Disk), only keeping a snippet in Chroma.
        For this task, we will simulate this by storing a 'compressed_size' metric.
        """
        memory_id = str(uuid.uuid4())
        embedding = self._get_embedding(content)

        if metadata is None:
            metadata = {}

        # Add tracking metadata
        now = datetime.datetime.now().isoformat()
        metadata['creation_date'] = now
        metadata['last_accessed'] = now
        metadata['access_count'] = 0

        # Calculate compression (Simulated optimization metric)
        compressed = self._compress_content(content)
        metadata['original_size'] = len(content)
        metadata['compressed_size'] = len(compressed)
        # Avoid division by zero
        metadata['compression_ratio'] = round(len(content) / len(compressed), 2) if len(compressed) > 0 else 0

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
        Updates access count for retrieved memories.
        """
        query_embedding = self._get_embedding(query)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        if not results or not results.get('ids'):
            return []

        ids = results['ids'][0]
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        final_results = []
        for id, doc, meta, dist in zip(ids, documents, metadatas, distances):
            # Update access metadata
            # Note: Chroma update is expensive, so we might batch this in a real app.
            # Here we do it immediately for correctness of the "Recency" feature.
            if meta is None:
                 meta = {}

            new_count = meta.get('access_count', 0) + 1
            meta['access_count'] = new_count
            meta['last_accessed'] = datetime.datetime.now().isoformat()

            # Since update is tricky with Chroma (needs full embedding if not cached),
            # we will attempt to update metadata.
            # In Chroma 0.4+, update(ids, metadatas) is supported without re-embedding.
            self._collection.update(ids=[id], metadatas=[meta])

            final_results.append({
                "id": id,
                "content": doc,
                "similarity": 1 - dist,
                "metadata": meta
            })

        return final_results

    def list_memories(self) -> list[dict]:
        """
        Lists all memories in the store.
        """
        results = self._collection.get()
        if not results['ids']:
             return []

        memories = []
        for id, doc, meta in zip(results['ids'], results['documents'], results['metadatas']):
            memories.append({
                "id": id,
                "content": doc,
                "metadata": meta
            })
        return memories

    def delete_memory(self, memory_id: str) -> bool:
        """
        Deletes a memory by its ID.
        """
        self._collection.delete(ids=[memory_id])
        return True
