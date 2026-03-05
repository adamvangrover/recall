import datetime
import math
from memory.local_vector_store.vector_memory_store import VectorMemoryStore

class ContextManager:
    def __init__(self, memory_store: VectorMemoryStore):
        self.memory_store = memory_store

    def calculate_recall_score(self, memory: dict, context_query: str) -> float:
        """
        Calculates a 'Recall Score' combining:
        - Vector Similarity (from search)
        - Recency (Exponential decay)
        - Frequency (Logarithmic boost)
        """
        similarity = memory.get('similarity', 0.5)
        metadata = memory.get('metadata', {}) or {}

        # Recency
        last_accessed = metadata.get('last_accessed')
        recency_score = 0.0
        if last_accessed:
            try:
                last = datetime.datetime.fromisoformat(last_accessed)
                now = datetime.datetime.now()
                hours_diff = (now - last).total_seconds() / 3600
                # Decay: Halves every 24 hours
                recency_score = 1.0 / (1.0 + (hours_diff / 24.0))
            except ValueError:
                recency_score = 0.0

        # Frequency
        access_count = metadata.get('access_count', 0)
        # Boost: log(1 + count)
        # Assuming normalized count up to 10
        frequency_score = min(1.0, math.log(1 + access_count) / math.log(11))

        # Weighted Score
        # 50% Similarity, 30% Recency, 20% Frequency
        final_score = (0.5 * similarity) + (0.3 * recency_score) + (0.2 * frequency_score)

        return round(final_score, 4)

    def get_contextual_memories(self, context_query: str, top_k: int = 5) -> list:
        """
        Retrieves memories relevant to the context, re-ranked by Recall Score.
        """
        # 1. Get vector results (broad search)
        results = self.memory_store.search_memory(context_query, n_results=top_k * 2)

        # 2. Re-rank
        ranked = []
        for res in results:
            score = self.calculate_recall_score(res, context_query)
            res['recall_score'] = score
            ranked.append(res)

        # 3. Sort by new score
        ranked.sort(key=lambda x: x.get('recall_score', 0), reverse=True)

        return ranked[:top_k]

    def get_forgotten_memories(self, days: int = 30) -> list:
        """
        Spaced Repetition: Returns memories not accessed in `days`.
        """
        all_memories = self.memory_store.list_memories()
        forgotten = []
        now = datetime.datetime.now()

        for mem in all_memories:
            meta = mem.get('metadata', {}) or {}
            last = meta.get('last_accessed')

            check_date = None
            if last:
                try:
                    check_date = datetime.datetime.fromisoformat(last)
                except ValueError:
                    pass

            # If never accessed (but created long ago), count it
            if not check_date:
                created = meta.get('creation_date')
                if created:
                     try:
                        check_date = datetime.datetime.fromisoformat(created)
                     except ValueError:
                        pass

            if check_date:
                 if (now - check_date).days >= days:
                     forgotten.append(mem)

        return forgotten
