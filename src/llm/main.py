def add_memory(memory):
    """Adds a memory to the LLM."""
    print(f"Adding memory to LLM: {memory}")
    return True

def search_memory(query):
    """Searches for a memory in the LLM."""
    print(f"Searching for memory in LLM: {query}")
    return [f"Found memory for '{query}'"]

def list_memories():
    """Lists all memories in the LLM."""
    print("Listing all memories from LLM")
    return ["memory 1", "memory 2", "memory 3"]

def delete_memory(id):
    """Deletes a memory from the LLM."""
    print(f"Deleting memory with ID from LLM: {id}")
    return True
