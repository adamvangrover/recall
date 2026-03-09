import datetime
import os
import networkx as nx
from src.memory.nlp_utils import NLPUtils
from src.memory.context import ContextManager
from src.memory.knowledge_graph import KnowledgeGraph
from src.memory.optimizer import MemoryOptimizer

def test_nlp_utils():
    text = "Hello #World. This is a Test sentence about Agentic AI. It should be summarized properly."
    data = NLPUtils.auto_process(text)

    tags = data['tags']
    assert 'world' in tags
    assert 'hello' in tags or 'test' in tags or 'agentic' in tags or 'ai' in tags

    summary = data['summary']
    assert summary == "Hello #World."

def test_contextual_ranking():
    now = datetime.datetime.now()
    memories = [
        {
            "id": "1", "similarity": 0.9,
            "metadata": {"access_count": 10, "last_accessed": now.isoformat()} # High sim, high recency, high freq
        },
        {
            "id": "2", "similarity": 0.9,
            "metadata": {"access_count": 1, "last_accessed": (now - datetime.timedelta(days=29)).isoformat()} # High sim, low recency, low freq
        },
        {
            "id": "3", "similarity": 0.1,
            "metadata": {"access_count": 10, "last_accessed": now.isoformat()} # Low sim, high recency, high freq
        }
    ]

    ranked = ContextManager.rank_memories(memories)

    assert ranked[0]['id'] == "1" # Should be first
    assert ranked[0]['composite_score'] > ranked[1]['composite_score']
    assert ranked[0]['composite_score'] > ranked[2]['composite_score']

def test_knowledge_graph(tmpdir):
    graph_path = os.path.join(tmpdir, "test_graph.pkl")
    kg = KnowledgeGraph(path=graph_path)

    kg.add_link("A", "B", "caused_by")
    kg.add_link("B", "C", "related_to")

    related = kg.get_related("A", max_depth=1)
    assert len(related) == 1
    assert related[0]['id'] == "B"

    related_depth_2 = kg.get_related("A", max_depth=2)
    assert len(related_depth_2) == 2
    ids = [r['id'] for r in related_depth_2]
    assert "B" in ids
    assert "C" in ids

    vis = kg.visualize("B")
    assert "A" in vis
    assert "C" in vis
    assert "caused_by" in vis
    assert "related_to" in vis

def test_memory_optimizer():
    now = datetime.datetime.now()
    memories = [
        {
            "id": "cold_mem",
            "metadata": {
                "last_accessed": (now - datetime.timedelta(days=40)).isoformat(),
                "original_size": 100,
                "compressed_size": 40
            }
        },
        {
            "id": "hot_mem",
            "metadata": {
                "last_accessed": now.isoformat(),
                "original_size": 200,
                "compressed_size": 80
            }
        }
    ]

    results = MemoryOptimizer.identify_cold_memories(memories, days_inactive=30)

    assert results["cold_count"] == 1
    assert results["cold_memories"][0]["id"] == "cold_mem"
    assert results["total_original_bytes"] == 100
    assert results["total_compressed_bytes"] == 40
    assert results["potential_savings_bytes"] == 60
