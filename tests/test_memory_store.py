import unittest
import os
from src.memory.local_store import MemoryStore

class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.test_path = 'test_memory.pkl'
        self.store = MemoryStore(storage_path=self.test_path)

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_add_memory(self):
        self.store.add_memory("test content")
        memories = self.store.list_memories()
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].content, "test content")

    def test_delete_memory(self):
        memory = self.store.add_memory("to be deleted")
        self.store.delete_memory(memory.id)
        memories = self.store.list_memories()
        self.assertEqual(len(memories), 0)

    def test_persistence(self):
        memory = self.store.add_memory("persistent content")

        # Create a new store instance to load from the file
        new_store = MemoryStore(storage_path=self.test_path)
        memories = new_store.list_memories()

        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].content, "persistent content")
        self.assertEqual(memories[0].id, memory.id)

if __name__ == '__main__':
    unittest.main()
