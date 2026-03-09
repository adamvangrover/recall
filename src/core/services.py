from src.memory.vector_store import VectorMemoryStore
from src.memory.knowledge_graph import KnowledgeGraph
from src.memory.context import ContextManager
from src.memory.optimizer import MemoryOptimizer

# Instantiate the single, persistent stores for the application
memory_store = VectorMemoryStore()
knowledge_graph = KnowledgeGraph()

def add_memory(content: str) -> str:
    """
    Adds a memory to the vector store and returns its ID.
    """
    return memory_store.add_memory(content)

def search_memory(query: str) -> list[dict]:
    """
    Performs a semantic search for memories, returning contextually ranked results.
    """
    results = memory_store.search_memory(query, n_results=10) # Get more initially to rank
    return ContextManager.rank_memories(results)

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

def link_memories(source_id: str, target_id: str, relation: str = "related_to") -> bool:
    """
    Links two memories in the knowledge graph.
    """
    knowledge_graph.add_link(source_id, target_id, relation)
    return True

def get_memory_graph(memory_id: str) -> str:
    """
    Gets the visual graph representation for a memory.
    """
    return knowledge_graph.visualize(memory_id)

def get_related_memories(memory_id: str) -> list[dict]:
    """
    Gets memories related to the given memory ID.
    """
    related_nodes = knowledge_graph.get_related(memory_id)
    results = []
    for node in related_nodes:
        mem = memory_store.get_memory(node["id"])
        if mem:
            results.append(mem)
    return results

def optimize_memory_storage(days_inactive: int = 30) -> dict:
    """
    Scans for cold memories and calculates potential savings.
    """
    all_memories = memory_store.list_memories(include_metadata=True)
    return MemoryOptimizer.identify_cold_memories(all_memories, days_inactive)

def get_forgotten_memories() -> list[dict]:
    """
    Identifies forgotten memories for spaced repetition.
    """
    all_memories = memory_store.list_memories(include_metadata=True)
    return ContextManager.get_forgotten_memories(all_memories)
