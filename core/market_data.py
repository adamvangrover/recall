import datetime
import random
import math
from typing import List, Dict

class MarketDataService:
    def __init__(self):
        pass

    def _get_consistent_price(self, ticker: str, date: datetime.date) -> float:
        """
        Generates a procedurally consistent price for a ticker on a given date.
        Model: Exponential Drift + Sine Wave + Daily Noise.
        """
        epoch = datetime.date(2020, 1, 1)
        days_delta = (date - epoch).days

        # Base parameters derived from ticker string
        # We use a stable seed based on the ticker name
        seed_val = sum(ord(c) for c in ticker)
        random.seed(seed_val)

        base_price = random.uniform(50, 200)
        drift = random.uniform(-0.0002, 0.0005) # Daily drift
        volatility = random.uniform(0.01, 0.03) # Daily vol
        period = random.uniform(100, 365) # Market cycle in days
        phase = random.uniform(0, 2 * math.pi)

        # Deterministic trend + cycle
        trend = base_price * math.exp(drift * days_delta)
        cycle = 1 + 0.15 * math.sin((2 * math.pi / period) * days_delta + phase)

        price = trend * cycle

        # Deterministic daily noise
        # Seed must be unique per ticker+date
        random.seed(f"{ticker}_{date.toordinal()}")
        noise = random.uniform(-volatility, volatility)

        final_price = price * (1 + noise)
        return max(0.01, round(final_price, 2))

    def get_price(self, ticker: str, date: datetime.date = None) -> float:
        """
        Gets the price of a ticker on a specific date.
        If date is None, returns current price.
        """
        if date is None:
            date = datetime.date.today()
        return self._get_consistent_price(ticker, date)

    def get_historical_prices(self, ticker: str, days: int, end_date: datetime.date = None) -> List[Dict]:
        """
        Returns a list of historical prices for the `days` leading up to `end_date`.
        Format: [{'date': 'YYYY-MM-DD', 'price': 123.45}, ...]
        Chronological order: Oldest to Newest.
        """
        if end_date is None:
            end_date = datetime.date.today()

        history = []
        for i in range(days):
             # 0 days ago = end_date
             # i days ago
             date = end_date - datetime.timedelta(days=i)
             price = self._get_consistent_price(ticker, date)
             history.append({'date': date.isoformat(), 'price': price})

        # History is [End, End-1, ...]
        # Reverse to [Oldest, ..., End]
        return history[::-1]
