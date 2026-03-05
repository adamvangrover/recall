from core.market_data import MarketDataService
from core.pricing import PricingEngine
from core.risk import RiskEngine
from core.rating import CreditRatingEngine
from core.analytics import BacktestEngine
from strategy.alpha import AlphaSignalGenerator
from memory.profile.manager import ProfileManager
from memory.sync_interface.services import get_store, list_memories, search_memory
from memory.knowledge_graph import KnowledgeGraph
from memory.context import ContextManager
from memory.optimizer import MemoryOptimizer
import datetime

# --- Engine Instantiation ---
market_data = MarketDataService()
pricing_engine = PricingEngine()
risk_engine = RiskEngine()
rating_engine = CreditRatingEngine()
signal_generator = AlphaSignalGenerator()
backtest_engine = BacktestEngine()
profile_manager = ProfileManager()

# --- Memory Services ---
memory_store = get_store()
knowledge_graph = KnowledgeGraph()
context_manager = ContextManager(memory_store)
memory_optimizer = MemoryOptimizer(memory_store)


# --- Tool Wrappers ---

def get_market_price(ticker: str):
    """Get the current market price for a ticker."""
    return market_data.get_price(ticker)

def calculate_option_price(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call'):
    """Calculate option price using Black-Scholes."""
    return pricing_engine.calculate_price('option', {
        'S': S, 'K': K, 'T': T, 'r': r, 'sigma': sigma, 'type': option_type
    })

def calculate_option_greeks(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call'):
    """Calculate option Greeks using Black-Scholes."""
    return pricing_engine.calculate_greeks('option', {
        'S': S, 'K': K, 'T': T, 'r': r, 'sigma': sigma, 'type': option_type
    })

def calculate_portfolio_risk(portfolio: list):
    """Calculate risk metrics for a portfolio."""
    return risk_engine.calculate_risk_metrics(portfolio)

def get_credit_rating(entity: str):
    """Get the credit rating for an entity."""
    return rating_engine.get_rating(entity)

def get_alpha_signal(ticker: str):
    """Get a trading signal for a ticker."""
    return signal_generator.generate_signal(ticker)

def run_backtest(ticker: str, days: int = 365, initial_capital: float = 100000.0):
    """Run a backtest for the default strategy on a ticker."""
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    return backtest_engine.run(signal_generator, ticker, start_date, end_date, initial_capital)

def get_user_watchlist():
    """Get the user's watchlist."""
    return profile_manager.get_watchlist()

def add_ticker_to_watchlist(ticker: str):
    """Add a ticker to the watchlist."""
    profile_manager.add_to_watchlist(ticker)
    return f"Added {ticker} to watchlist."

def get_user_portfolio():
    """Get the user's portfolio."""
    return profile_manager.get_portfolio()

def add_portfolio_position(symbol: str, quantity: float, price: float):
    """Add a position to the portfolio."""
    profile_manager.add_position(symbol, quantity, price)
    return f"Added {quantity} shares of {symbol} at ${price}."

# --- Advanced Memory Tools ---

def link_memories(id1: str, id2: str, relation: str = "related"):
    """Link two memories in the Knowledge Graph."""
    knowledge_graph.link_memories(id1, id2, relation)
    return f"Linked {id1} to {id2} as '{relation}'."

def get_related_memories(memory_id: str):
    """Get related memories from the Knowledge Graph."""
    return knowledge_graph.get_related(memory_id)

def get_contextual_memories(context: str):
    """Get memories relevant to the current context (ranked by score)."""
    return context_manager.get_contextual_memories(context)

def optimize_memory_storage():
    """Run the memory optimizer."""
    return memory_optimizer.optimize_storage()
