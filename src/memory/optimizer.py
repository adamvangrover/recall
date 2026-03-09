import datetime

class MemoryOptimizer:
    @staticmethod
    def identify_cold_memories(memories: list[dict], days_inactive: int = 30) -> dict:
        """
        Scans for 'Cold' memories unused for N days and calculates potential storage savings.
        """
        now = datetime.datetime.now()
        cold_memories = []
        total_original_bytes = 0
        total_compressed_bytes = 0

        for m in memories:
            meta = m.get('metadata', {})
            last_acc_str = meta.get('last_accessed')

            is_cold = False
            if last_acc_str:
                try:
                    last_acc = datetime.datetime.fromisoformat(last_acc_str)
                    days_diff = (now - last_acc).days
                    if days_diff >= days_inactive:
                        is_cold = True
                except ValueError:
                    pass
            else:
                # If no access date, assume cold if old enough based on creation
                creation_str = meta.get('creation_date')
                if creation_str:
                    try:
                        creation = datetime.datetime.fromisoformat(creation_str)
                        days_diff = (now - creation).days
                        if days_diff >= days_inactive:
                            is_cold = True
                    except ValueError:
                        pass

            if is_cold:
                cold_memories.append(m)
                total_original_bytes += meta.get('original_size', 0)
                total_compressed_bytes += meta.get('compressed_size', 0)

        savings_bytes = total_original_bytes - total_compressed_bytes

        return {
            "cold_memories": cold_memories,
            "cold_count": len(cold_memories),
            "potential_savings_bytes": savings_bytes,
            "total_original_bytes": total_original_bytes,
            "total_compressed_bytes": total_compressed_bytes
        }
