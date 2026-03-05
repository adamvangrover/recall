import re
import collections

class NLPUtils:
    def __init__(self):
        pass

    def summarize(self, text: str, sentences: int = 1) -> str:
        """
        Simple heuristic summarizer.
        Returns the first few sentences.
        """
        # Split by .!?
        sents = re.split(r'[.!?]+', text)
        sents = [s.strip() for s in sents if s.strip()]

        if not sents:
            return text[:50] + "..."

        summary = ". ".join(sents[:sentences])
        if len(sents) > sentences:
            summary += "..."

        return summary

    def extract_tags(self, text: str, top_n: int = 3) -> list:
        """
        Extracts tags based on capitalized words (Proper Nouns heuristic)
        and frequent significant words.
        """
        # Simple tokenization
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return []

        # 1. Capitalized words (potential entities)
        # Exclude start of sentence if possible, but simpler here:
        # Just find all caps that aren't stop words
        caps = [w for w in words if w[0].isupper() and len(w) > 2]

        # 2. Frequent words
        # Basic stop list
        stops = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'at', 'by', 'an', 'be', 'this', 'that', 'from', 'it'}
        filtered = [w.lower() for w in words if w.lower() not in stops and len(w) > 3]

        counter = collections.Counter(filtered)
        freq_tags = [item[0] for item in counter.most_common(top_n)]

        # Combine
        combined = list(set(caps + freq_tags))
        return combined[:top_n]
