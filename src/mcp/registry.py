from . import tools

TOOL_REGISTRY = {
    "search_memory": tools.search_recall_memory,
    "add_memory": tools.save_recall_memory,
}

def get_tool(name: str):
    return TOOL_REGISTRY.get(name)

def list_tools():
    return list(TOOL_REGISTRY.keys())
