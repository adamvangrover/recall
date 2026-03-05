import datetime
from memory.local_vector_store.vector_memory_store import VectorMemoryStore

class MemoryOptimizer:
    def __init__(self, store: VectorMemoryStore):
        self.store = store

    def optimize_storage(self, archive_days: int = 90) -> dict:
        """
        Scans memory store for "Cold" memories (not accessed in `archive_days`)
        and calculates potential savings.
        In a real system, this would move them to S3/Glacier.
        """
        memories = self.store.list_memories()

        total_original = 0
        total_compressed = 0
        cold_count = 0
        cold_size = 0

        now = datetime.datetime.now()

        for mem in memories:
            meta = mem.get('metadata', {}) or {}
            content = mem.get('content', '')

            orig = meta.get('original_size', len(content))
            comp = meta.get('compressed_size', len(content)) # Fallback if no compression data

            total_original += orig
            total_compressed += comp

            # Check Cold
            last = meta.get('last_accessed')
            if last:
                try:
                    last_dt = datetime.datetime.fromisoformat(last)
                    if (now - last_dt).days > archive_days:
                        cold_count += 1
                        cold_size += comp
                except ValueError:
                    pass
            elif meta.get('creation_date'): # Use creation if no last accessed
                 try:
                    last_dt = datetime.datetime.fromisoformat(meta['creation_date'])
                    if (now - last_dt).days > archive_days:
                        cold_count += 1
                        cold_size += comp
                 except ValueError:
                     pass

        total_savings = total_original - total_compressed
        compression_ratio = total_original / total_compressed if total_compressed > 0 else 1.0

        return {
            "total_memories": len(memories),
            "total_size_original": total_original,
            "total_size_compressed": total_compressed,
            "space_saved": total_savings,
            "compression_ratio": round(compression_ratio, 2),
            "cold_memories_count": cold_count,
            "cold_memories_size": cold_size,
            "recommendation": f"Archive {cold_count} memories to save {cold_size} bytes." if cold_count > 0 else "Storage is optimal."
        }
