import networkx as nx
import json
import os
from networkx.readwrite import json_graph

class KnowledgeGraph:
    def __init__(self, path="~/.recall_graph.json"):
        self.path = os.path.expanduser(path)
        self.graph = nx.Graph()
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    data = json.load(f)
                    self.graph = json_graph.node_link_graph(data)
            except (json.JSONDecodeError, IndexError):
                self.graph = nx.Graph()
        else:
            self.graph = nx.Graph()

    def _save(self):
        data = json_graph.node_link_data(self.graph)
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def link_memories(self, id1: str, id2: str, relationship: str = "related"):
        """
        Creates a link between two memories with a relationship type.
        """
        if not self.graph.has_node(id1):
             self.graph.add_node(id1)
        if not self.graph.has_node(id2):
             self.graph.add_node(id2)

        self.graph.add_edge(id1, id2, relation=relationship)
        self._save()

    def get_related(self, memory_id: str, depth: int = 1) -> list:
        """
        Returns a list of related memory IDs within `depth` hops.
        """
        if memory_id not in self.graph:
            return []

        # Use ego_graph to find neighbors within depth
        subgraph = nx.ego_graph(self.graph, memory_id, radius=depth)
        nodes = list(subgraph.nodes())

        # Remove self
        if memory_id in nodes:
            nodes.remove(memory_id)

        return nodes

    def get_graph_stats(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph)
        }
