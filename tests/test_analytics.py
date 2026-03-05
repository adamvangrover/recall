import pytest
import os
import datetime
from core.analytics import BacktestEngine
from strategy.alpha import AlphaSignalGenerator
from memory.profile.manager import ProfileManager

def test_backtest_run():
    engine = BacktestEngine()
    strategy = AlphaSignalGenerator()
    end = datetime.date.today()
    start = end - datetime.timedelta(days=100)

    res = engine.run(strategy, "AAPL", start, end, 100000.0)

    assert res['ticker'] == "AAPL"
    assert res['initial_capital'] == 100000.0
    assert 'total_return_pct' in res
    assert 'sharpe_ratio' in res
    assert 'max_drawdown_pct' in res
    # Ensure trade log is present
    assert 'trade_log' in res

def test_profile_manager():
    # Use a temp file
    path = "test_profile.json"
    if os.path.exists(path):
        os.remove(path)

    pm = ProfileManager(path=path)

    pm.add_to_watchlist("TSLA")
    assert "TSLA" in pm.get_watchlist()

    pm.remove_from_watchlist("TSLA")
    assert "TSLA" not in pm.get_watchlist()

    pm.add_position("MSFT", 10, 150.0)
    pf = pm.get_portfolio()
    assert len(pf) == 1
    assert pf[0]['symbol'] == "MSFT"
    assert pf[0]['quantity'] == 10

    # Add more to average
    pm.add_position("MSFT", 10, 250.0)
    pf = pm.get_portfolio()
    assert pf[0]['quantity'] == 20
    assert pf[0]['avg_price'] == 200.0

    if os.path.exists(path):
        os.remove(path)
