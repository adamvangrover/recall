from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text.
        """
        if not text:
            return []

        embedding = self.model.encode(text)
        return embedding.tolist()
