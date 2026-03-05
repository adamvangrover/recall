import random
import datetime

class CreditRatingEngine:
    def __init__(self):
        pass

    def get_rating(self, entity_name: str) -> dict:
        """
        Simulates retrieving a credit rating for an entity.
        """
        # Deterministic random based on name
        random.seed(entity_name)
        ratings = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'B', 'CCC']
        rating = random.choice(ratings)

        return {
            'entity': entity_name,
            'rating': rating,
            'outlook': random.choice(['Stable', 'Positive', 'Negative']),
            'date': datetime.date.today().isoformat()
        }
