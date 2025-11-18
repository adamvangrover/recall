import unittest
from src.core.vector_memory_store import VectorMemoryStore
import chromadb

class TestVectorMemoryStore(unittest.TestCase):
    def setUp(self):
        # Create an in-memory instance of ChromaDB for each test
        self.client = chromadb.Client()
        self.collection_name = "test_memories"

        # Instantiate the store and override its internal client
        self.store = VectorMemoryStore()
        self.store._client = self.client
        self.store._collection = self.client.get_or_create_collection(name=self.collection_name)

    def tearDown(self):
        # Clean up the collection after each test to ensure test isolation
        self.client.delete_collection(name=self.collection_name)

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

        # Since we use a placeholder embedding, search is not truly semantic.
        # This test just ensures the search function returns results in the correct format.
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
