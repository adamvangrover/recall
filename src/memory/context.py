import datetime

class ContextManager:
    @staticmethod
    def rank_memories(memories: list[dict]) -> list[dict]:
        """
        Ranks memories based on a composite score:
        50% Similarity
        30% Recency
        20% Frequency
        """
        if not memories:
            return []

        now = datetime.datetime.now()

        # We need to normalize recency and frequency
        # For simplicity, let's say recency score is maxed out at 1.0 for now
        # and degrades to 0.0 over 30 days
        max_days = 30.0

        # Find max frequency for normalization
        max_freq = 1
        for m in memories:
            meta = m.get('metadata', {})
            freq = meta.get('access_count', 1)
            if freq > max_freq:
                max_freq = freq

        for m in memories:
            meta = m.get('metadata', {})

            # Similarity (assumed to be 0-1 from vector store)
            sim = m.get('similarity', 0.0)

            # Recency
            last_acc_str = meta.get('last_accessed')
            recency_score = 0.0
            if last_acc_str:
                try:
                    last_acc = datetime.datetime.fromisoformat(last_acc_str)
                    days_diff = (now - last_acc).days
                    recency_score = max(0.0, 1.0 - (days_diff / max_days))
                except ValueError:
                    pass

            # Frequency
            freq = meta.get('access_count', 1)
            freq_score = freq / max_freq

            # Composite Score
            score = (0.5 * sim) + (0.3 * recency_score) + (0.2 * freq_score)
            m['composite_score'] = score

        # Sort descending
        memories.sort(key=lambda x: x.get('composite_score', 0), reverse=True)
        return memories

    @staticmethod
    def get_forgotten_memories(memories: list[dict], days_threshold: int = 14, min_access: int = 2) -> list[dict]:
        """
        Identifies memories that haven't been accessed in a while but were previously accessed.
        (Spaced Repetition logic).
        """
        forgotten = []
        now = datetime.datetime.now()

        for m in memories:
            meta = m.get('metadata', {})
            freq = meta.get('access_count', 0)

            if freq >= min_access:
                last_acc_str = meta.get('last_accessed')
                if last_acc_str:
                    try:
                        last_acc = datetime.datetime.fromisoformat(last_acc_str)
                        days_diff = (now - last_acc).days
                        if days_diff >= days_threshold:
                            forgotten.append(m)
                    except ValueError:
                        pass

        return forgotten
