import uuid
import pickle
import os

class Memory:
    def __init__(self, content):
        self.id = str(uuid.uuid4())
        self.content = content

class MemoryStore:
    def __init__(self, storage_path='~/.recall_memory.pkl'):
        self._storage_path = os.path.expanduser(storage_path)
        self._memories = self._load_memories()

    def _load_memories(self):
        if os.path.exists(self._storage_path):
            with open(self._storage_path, 'rb') as f:
                try:
                    return pickle.load(f)
                except EOFError:
                    return []
        return []

    def _save_memories(self):
        with open(self._storage_path, 'wb') as f:
            pickle.dump(self._memories, f)

    def add_memory(self, content):
        memory = Memory(content)
        self._memories.append(memory)
        self._save_memories()
        return memory

    def get_memory(self, id):
        for memory in self._memories:
            if str(memory.id) == str(id):
                return memory
        return None

    def list_memories(self):
        return self._memories

    def delete_memory(self, id):
        memory = self.get_memory(id)
        if memory:
            self._memories.remove(memory)
            self._save_memories()
            return True
        return False
