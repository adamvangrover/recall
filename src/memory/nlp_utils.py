import re
from typing import List, Dict

class NLPUtils:
    @staticmethod
    def extract_tags(text: str) -> List[str]:
        """
        Extracts tags based on capitalized words or hashtags.
        """
        if not text:
            return []

        # Extract hashtags
        hashtags = re.findall(r'#(\w+)', text)

        # Extract capitalized words (heuristic for proper nouns/keywords)
        # Ignore common words at the start of sentences
        words = re.findall(r'\b[A-Z][a-z]+\b', text)

        # Combine, lowercase, and unique
        tags = set([tag.lower() for tag in hashtags + words])

        # Filter out too short tags or common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'it', 'this', 'that'}
        tags = {tag for tag in tags if len(tag) > 2 and tag not in stop_words}

        return list(tags)

    @staticmethod
    def summarize(text: str, max_length: int = 50) -> str:
        """
        Provides a basic heuristic summary (first sentence or truncated).
        """
        if not text:
            return ""

        # Try to get the first sentence
        match = re.search(r'^(.*?[.!?])', text)
        if match:
            sentence = match.group(1).strip()
            if len(sentence) <= max_length:
                return sentence

        # Fallback to truncation
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    @staticmethod
    def auto_process(text: str) -> Dict[str, any]:
        """
        Returns tags and summary.
        """
        return {
            "tags": NLPUtils.extract_tags(text),
            "summary": NLPUtils.summarize(text)
        }
