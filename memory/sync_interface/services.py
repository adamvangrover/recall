from memory.local_vector_store.vector_memory_store import VectorMemoryStore
from memory.nlp_utils import NLPUtils

# Instantiate the single, persistent VectorMemoryStore for the application
memory_store = VectorMemoryStore()
nlp = NLPUtils()

def add_memory(content: str) -> str:
    """
    Adds a memory to the vector store with auto-summary and tags.
    """
    summary = nlp.summarize(content)
    tags = nlp.extract_tags(content)

    metadata = {
        'summary': summary,
        'tags': ",".join(tags)
    }

    return memory_store.add_memory(content, metadata=metadata)

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

def get_store():
    return memory_store
