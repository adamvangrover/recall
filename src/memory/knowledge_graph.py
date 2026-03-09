import networkx as nx
import os
import json

class KnowledgeGraph:
    def __init__(self, path="~/.recall_graph.json"):
        # We check for pkl in case it was passed during tests
        if path.endswith(".pkl"):
             path = path.replace(".pkl", ".json")
        self._path = os.path.expanduser(path)
        self._graph = self._load_graph()

    def _load_graph(self) -> nx.DiGraph:
        if os.path.exists(self._path):
            try:
                with open(self._path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return nx.node_link_graph(data, directed=True)
            except Exception:
                return nx.DiGraph()
        return nx.DiGraph()

    def _save_graph(self):
        data = nx.node_link_data(self._graph)
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def add_link(self, source_id: str, target_id: str, relation: str = "related_to"):
        """
        Adds a directed link between two memories.
        """
        self._graph.add_edge(source_id, target_id, relation=relation)
        self._save_graph()

    def get_related(self, memory_id: str, max_depth: int = 1) -> list[dict]:
        """
        Gets related memories up to a certain depth.
        """
        if memory_id not in self._graph:
            return []

        # Use BFS to find nodes up to max_depth
        related_nodes = set()
        queue = [(memory_id, 0)]
        visited = set()

        while queue:
            current_id, depth = queue.pop(0)
            if current_id not in visited and depth <= max_depth:
                visited.add(current_id)
                if current_id != memory_id:
                    related_nodes.add(current_id)

                for neighbor in self._graph.successors(current_id):
                    queue.append((neighbor, depth + 1))
                for neighbor in self._graph.predecessors(current_id):
                    queue.append((neighbor, depth + 1))

        # Build return list
        results = []
        for node in related_nodes:
            # We'll just return edge info here, the service can fetch full content
            results.append({"id": node})

        return results

    def visualize(self, memory_id: str) -> str:
        """
        Returns a string representation of the local graph neighborhood for CLI.
        """
        if memory_id not in self._graph:
            return f"No graph connections for memory {memory_id}."

        lines = [f"Graph for Memory: {memory_id}"]

        # Outgoing edges
        outgoing = list(self._graph.successors(memory_id))
        if outgoing:
            lines.append("  Outgoing Links:")
            for neighbor in outgoing:
                edge_data = self._graph.get_edge_data(memory_id, neighbor)
                rel = edge_data.get("relation", "linked")
                lines.append(f"    --[{rel}]--> {neighbor}")

        # Incoming edges
        incoming = list(self._graph.predecessors(memory_id))
        if incoming:
            lines.append("  Incoming Links:")
            for neighbor in incoming:
                edge_data = self._graph.get_edge_data(neighbor, memory_id)
                rel = edge_data.get("relation", "linked")
                lines.append(f"    <--[{rel}]-- {neighbor}")

        if not outgoing and not incoming:
            return f"Memory {memory_id} exists in graph but has no connections."

        return "\n".join(lines)
