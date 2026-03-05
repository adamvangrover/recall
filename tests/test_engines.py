import pytest
from core.market_data import MarketDataService
from core.pricing import PricingEngine
from core.risk import RiskEngine
from core.rating import CreditRatingEngine
from strategy.alpha import AlphaSignalGenerator

def test_market_data():
    service = MarketDataService()
    price = service.get_price("AAPL")
    assert price > 0

    # 5 days
    history = service.get_historical_prices("AAPL", 5)
    assert len(history) == 5
    # Chronological order check: Oldest first
    # history[0] is oldest, history[-1] is newest
    assert history[0]['date'] < history[-1]['date']

def test_pricing():
    engine = PricingEngine()
    # Call option ITM
    price = engine.calculate_price('option', {
        'S': 100, 'K': 90, 'T': 1, 'r': 0.05, 'sigma': 0.2, 'type': 'call'
    })
    # Intrinsic value is 10. Time value should make it > 10.
    assert price > 10

    # Put option OTM
    price = engine.calculate_price('option', {
        'S': 100, 'K': 90, 'T': 1, 'r': 0.05, 'sigma': 0.2, 'type': 'put'
    })
    # Should be relatively low but positive
    assert price > 0
    assert price < 10

def test_greeks():
    engine = PricingEngine()
    # ATM Call: S=100, K=100, T=1, r=0.05, vol=0.2
    greeks = engine.calculate_greeks('option', {
        'S': 100, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.2, 'type': 'call'
    })
    assert 'delta' in greeks
    # Delta for ATM call is roughly 0.5 + small drift adjustment (N(d1))
    # d1 ~ (0.05 + 0.5*0.04) / 0.2 = 0.07 / 0.2 = 0.35. N(0.35) > 0.5
    assert greeks['delta'] > 0.5
    assert greeks['gamma'] > 0
    assert greeks['vega'] > 0
    # Theta is usually negative for long calls
    assert greeks['theta'] < 0

def test_risk():
    engine = RiskEngine()
    portfolio = [{'symbol': 'A', 'value': 1000}, {'symbol': 'B', 'value': 2000}]
    metrics = engine.calculate_risk_metrics(portfolio)
    assert metrics['total_value'] == 3000
    assert 'VaR_95' in metrics

def test_risk_performance_metrics():
    engine = RiskEngine()
    # 4 days of returns
    returns = [0.01, 0.02, -0.01, 0.005]
    metrics = engine.calculate_performance_metrics(returns)
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics
    assert metrics['annualized_return'] != 0

def test_rating():
    engine = CreditRatingEngine()
    rating = engine.get_rating("MyCompany")
    assert 'rating' in rating
    assert rating['entity'] == "MyCompany"

def test_strategy():
    gen = AlphaSignalGenerator()
    signal = gen.generate_signal("TSLA")
    assert signal['ticker'] == "TSLA"
    assert signal['signal'] in ['BUY', 'SELL', 'HOLD']
    assert 'sma_5' in signal
    assert 'sma_20' in signal
