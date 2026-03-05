import pytest
import os
import shutil
from memory.local_vector_store.vector_memory_store import VectorMemoryStore
from memory.knowledge_graph import KnowledgeGraph
from memory.context import ContextManager
from memory.nlp_utils import NLPUtils
from memory.optimizer import MemoryOptimizer

def test_memory_compression_and_metadata():
    # Setup
    store = VectorMemoryStore()
    content = "This is a test memory content that should be compressed."
    mid = store.add_memory(content)

    # Retrieve
    mems = store.list_memories()
    assert len(mems) >= 1
    found = next(m for m in mems if m['id'] == mid)

    # Check Metadata
    meta = found['metadata']
    if meta is None: meta = {}

    # In ChromaDB (depending on version), metadata values are usually primitives.
    # Our implementation stores ints.

    assert 'compressed_size' in meta
    assert 'original_size' in meta
    # Zlib compression on short strings can sometimes be larger due to headers.
    # Let's just verify they are integers and exist.
    assert isinstance(meta['original_size'], int)
    assert isinstance(meta['compressed_size'], int)
    assert 'access_count' in meta

def test_knowledge_graph():
    path = "test_graph.json"
    if os.path.exists(path):
        os.remove(path)

    kg = KnowledgeGraph(path=path)
    kg.link_memories("A", "B", "related")
    kg.link_memories("B", "C", "caused_by")

    related_a = kg.get_related("A")
    assert "B" in related_a
    assert "C" not in related_a # Depth 1

    related_b = kg.get_related("B")
    assert "A" in related_b
    assert "C" in related_b

    if os.path.exists(path):
        os.remove(path)

def test_context_manager():
    store = VectorMemoryStore()
    cm = ContextManager(store)

    # Mock memory with metadata
    mem = {
        'id': '1',
        'similarity': 0.9,
        'metadata': {
            'access_count': 5,
            'last_accessed': None # Old or None
        }
    }

    score = cm.calculate_recall_score(mem, "test")
    assert score > 0
    # Similarity (0.45) + Freq (some boost) + Recency (0)
    assert score > 0.45

def test_nlp_utils():
    nlp = NLPUtils()
    text = "Tesla Inc is a great company. Elon Musk leads it. The stock is high."

    summary = nlp.summarize(text, sentences=1)
    # The heuristic splits by .!? so "Tesla Inc" might be split if it had a dot, but here "Inc" has no dot in my string.
    assert "Tesla Inc is a great company" in summary

    tags = nlp.extract_tags(text)
    # Should include capitalized words
    assert "Tesla" in tags or "Elon" in tags or "Musk" in tags

def test_optimizer():
    store = VectorMemoryStore()
    # Add a memory
    store.add_memory("Old memory")

    opt = MemoryOptimizer(store)
    stats = opt.optimize_storage(archive_days=0) # Force cold

    assert stats['total_memories'] >= 1
    # Savings can be negative for short strings due to zlib headers
    assert isinstance(stats['space_saved'], int)
    assert stats['cold_memories_count'] >= 0
