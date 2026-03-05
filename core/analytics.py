import datetime
from core.market_data import MarketDataService
from core.risk import RiskEngine

class BacktestEngine:
    def __init__(self):
        self.risk_engine = RiskEngine()

    def run(self, strategy, ticker: str, start_date: datetime.date, end_date: datetime.date, initial_capital: float = 100000.0) -> dict:
        """
        Runs a backtest for a strategy on a single ticker.
        """
        capital = initial_capital
        position = 0.0 # Number of shares

        history = []
        portfolio_values = []
        daily_returns = []

        current_date = start_date
        while current_date <= end_date:
            # 1. Get Signal
            # Strategy must have generate_signal(ticker, date)
            signal_data = strategy.generate_signal(ticker, date=current_date)
            price = signal_data['current_price']
            signal = signal_data['signal']

            # 2. Execute (Simplified: All-in / All-out)
            if signal == 'BUY' and position == 0:
                # Buy as much as possible
                position = capital / price
                capital = 0.0
                history.append({'date': current_date.isoformat(), 'action': 'BUY', 'price': price, 'shares': round(position, 4)})
            elif signal == 'SELL' and position > 0:
                # Sell all
                capital = position * price
                position = 0.0
                history.append({'date': current_date.isoformat(), 'action': 'SELL', 'price': price, 'capital': round(capital, 2)})

            # 3. Track Value
            current_value = capital + (position * price)
            portfolio_values.append(current_value)

            if len(portfolio_values) > 1:
                daily_ret = (current_value - portfolio_values[-2]) / portfolio_values[-2]
                daily_returns.append(daily_ret)

            current_date += datetime.timedelta(days=1)

        # 4. Calculate Stats
        final_value = portfolio_values[-1] if portfolio_values else initial_capital
        total_return = (final_value - initial_capital) / initial_capital

        metrics = self.risk_engine.calculate_performance_metrics(daily_returns)

        return {
            'ticker': ticker,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'initial_capital': initial_capital,
            'final_value': round(final_value, 2),
            'total_return_pct': round(total_return * 100, 2),
            'sharpe_ratio': metrics['sharpe_ratio'],
            'max_drawdown_pct': round(metrics['max_drawdown'] * 100, 2),
            'trades_count': len(history),
            'trade_log': history
        }
