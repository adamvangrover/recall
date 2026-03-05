from core.market_data import MarketDataService
import datetime

class AlphaSignalGenerator:
    def __init__(self):
        self.market_data = MarketDataService()

    def generate_signal(self, ticker: str, date: datetime.date = None) -> dict:
        """
        Generates a trading signal (BUY/SELL/HOLD) based on moving averages.
        Optionally accepts a 'date' for backtesting.
        """
        if date is None:
            date = datetime.date.today()

        # Get 20 days history ending on 'date'
        history = self.market_data.get_historical_prices(ticker, 20, end_date=date)

        if len(history) < 20:
             return {'ticker': ticker, 'signal': 'HOLD', 'reason': 'Insufficient Data', 'date': date.isoformat()}

        prices = [item['price'] for item in history]
        sma_5 = sum(prices[-5:]) / 5
        sma_20 = sum(prices[-20:]) / 20

        current_price = prices[-1]

        signal = 'HOLD'
        confidence = 0.0

        if sma_5 > sma_20:
            signal = 'BUY'
            confidence = (sma_5 - sma_20) / sma_20
        elif sma_5 < sma_20:
            signal = 'SELL'
            confidence = (sma_20 - sma_5) / sma_20

        return {
            'ticker': ticker,
            'date': date.isoformat(),
            'signal': signal,
            'current_price': current_price,
            'sma_5': round(sma_5, 2),
            'sma_20': round(sma_20, 2),
            'confidence': round(confidence, 2)
        }
