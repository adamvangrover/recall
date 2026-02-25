from src.core.services import search_memory, add_memory

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
