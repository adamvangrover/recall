from src.core.vector_memory_store import VectorMemoryStore

# Instantiate the single, persistent VectorMemoryStore for the application
memory_store = VectorMemoryStore()

def add_memory(content: str) -> str:
    """
    Adds a memory to the vector store and returns its ID.
    """
    return memory_store.add_memory(content)

def search_memory(query: str) -> list[dict]:
    """
    Performs a semantic search for memories.
    """
    return memory_store.search_memory(query)

def list_memories() -> list[dict]:
    """
    Lists all memories.
    """
    return memory_store.list_memories()

def delete_memory(memory_id: str) -> bool:
    """
    Deletes a memory by its ID.
    """
    return memory_store.delete_memory(memory_id)
