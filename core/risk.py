import numpy as np

class RiskEngine:
    def __init__(self):
        pass

    def calculate_risk_metrics(self, portfolio: list) -> dict:
        """
        Calculates basic risk metrics for a portfolio.
        Portfolio is a list of positions, e.g., [{'symbol': 'AAPL', 'value': 15000}, ...]
        """
        total_value = sum(item.get('value', 0) for item in portfolio)

        # Simulated VaR (Value at Risk)
        # In real life this would use historical data and covariance matrices
        var_95 = total_value * 0.05
        var_99 = total_value * 0.07

        return {
            'total_value': total_value,
            'VaR_95': round(var_95, 2),
            'VaR_99': round(var_99, 2),
            'status': 'Within Limits' if total_value < 1000000 else 'Breach'
        }

    def calculate_performance_metrics(self, returns: list, risk_free_rate: float = 0.0) -> dict:
        """
        Calculates performance metrics (Sharpe, Max Drawdown) for a series of returns.
        returns: list of float (e.g., 0.01 for 1%)
        risk_free_rate: annual risk-free rate (decimal, e.g., 0.05)
        """
        if not returns:
            return {'sharpe_ratio': 0.0, 'max_drawdown': 0.0, 'annualized_return': 0.0, 'annualized_vol': 0.0}

        returns_arr = np.array(returns)

        # Annualized Return (assuming daily)
        mean_return = np.mean(returns_arr)
        annualized_return = mean_return * 252

        # Annualized Volatility
        std_dev = np.std(returns_arr)
        annualized_vol = std_dev * np.sqrt(252)

        # Sharpe Ratio
        rf_daily = risk_free_rate / 252
        excess_returns = returns_arr - rf_daily
        sharpe_ratio = 0.0
        if annualized_vol > 0:
            sharpe_ratio = (np.mean(excess_returns) * 252) / annualized_vol

        # Max Drawdown
        cum_returns = np.cumprod(1 + returns_arr)
        peak = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - peak) / peak
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0.0

        return {
            'sharpe_ratio': round(float(sharpe_ratio), 4),
            'max_drawdown': round(float(max_drawdown), 4),
            'annualized_return': round(float(annualized_return), 4),
            'annualized_vol': round(float(annualized_vol), 4)
        }
