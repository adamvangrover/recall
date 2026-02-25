from src.memory.local_store import MemoryStore

memory_store = MemoryStore()

def add_memory(content):
    """Adds a memory to the memory store."""
    memory = memory_store.add_memory(content)
    return memory is not None

def search_memory(query):
    """Searches for a memory in the memory store."""
    all_memories = memory_store.list_memories()
    results = [m for m in all_memories if query in m.content]
    return [f"{m.id}: {m.content}" for m in results]

def list_memories():
    """Lists all memories in the memory store."""
    memories = memory_store.list_memories()
    return [f"{m.id}: {m.content}" for m in memories]

def delete_memory(id):
    """Deletes a memory from the memory store."""
    return memory_store.delete_memory(id)
