import unittest
from unittest.mock import MagicMock
from src.memory.vector_store import VectorMemoryStore
import chromadb

class TestVectorMemoryStore(unittest.TestCase):
    def setUp(self):
        # Create an in-memory instance of ChromaDB for each test
        self.client = chromadb.Client()
        self.collection_name = "test_memories"

        # Instantiate the store
        # Note: This will load the EmbeddingService model which is slow.
        # Ideally we'd inject dependencies, but for now we patch it after init.
        self.store = VectorMemoryStore()
        self.store._client = self.client
        self.store._collection = self.client.get_or_create_collection(name=self.collection_name)

        # Mock embedding service to avoid model loading/inference
        self.store._embedding_service = MagicMock()
        # Mock return value to be a list of floats (size 384 for example)
        self.store._embedding_service.generate_embedding.return_value = [0.1] * 384

    def tearDown(self):
        # Clean up the collection after each test to ensure test isolation
        try:
            self.client.delete_collection(name=self.collection_name)
        except:
            pass

    def test_add_and_list_memory(self):
        """Tests that a memory can be added and then listed."""
        self.store.add_memory("test content")
        memories = self.store.list_memories()
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]['content'], "test content")

    def test_delete_memory(self):
        """Tests that a memory can be deleted."""
        memory_id = self.store.add_memory("to be deleted")

        # Verify it was added
        self.assertEqual(len(self.store.list_memories()), 1)

        # Delete it
        self.store.delete_memory(memory_id)

        # Verify it's gone
        memories = self.store.list_memories()
        self.assertEqual(len(memories), 0)

    def test_search_memory(self):
        """Tests the search functionality."""
        self.store.add_memory("I enjoy apples")
        self.store.add_memory("I enjoy bananas")

        results = self.store.search_memory("fruits")
        self.assertIsInstance(results, list)

        # The search should return some results
        self.assertGreater(len(results), 0)

        # Check the format of the first result
        self.assertIn('id', results[0])
        self.assertIn('content', results[0])
        self.assertIn('similarity', results[0])

if __name__ == '__main__':
    unittest.main()
