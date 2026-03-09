from src.core.services import search_memory, add_memory, link_memories as link_memories_service, get_related_memories as get_related_memories_service, optimize_memory_storage as optimize_memory_storage_service

def search_recall_memory(query: str, limit: int = 5) -> list[dict]:
    """
    Searches the Total Recall memory for relevant information.
    """
    results = search_memory(query)
    # Filter or format if necessary, but services returns list[dict]
    return results[:limit]

def save_recall_memory(content: str) -> str:
    """
    Saves a new memory to the Total Recall system.
    """
    return add_memory(content)

def link_memories(source_id: str, target_id: str, relation: str = "related_to") -> bool:
    """
    Links two memories explicitly.
    """
    return link_memories_service(source_id, target_id, relation)

def get_related_memories(memory_id: str) -> list[dict]:
    """
    Gets memories related to the specified memory ID.
    """
    return get_related_memories_service(memory_id)

def optimize_memory_storage(days_inactive: int = 30) -> dict:
    """
    Scans memory for storage optimization opportunities.
    """
    return optimize_memory_storage_service(days_inactive)
