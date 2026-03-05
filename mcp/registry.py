from mcp.tools import (
    get_market_price,
    calculate_option_price,
    calculate_option_greeks,
    calculate_portfolio_risk,
    get_credit_rating,
    get_alpha_signal,
    run_backtest,
    get_user_watchlist,
    add_ticker_to_watchlist,
    get_user_portfolio,
    add_portfolio_position,
    link_memories,
    get_related_memories,
    get_contextual_memories,
    optimize_memory_storage
)

TOOLS = {
    "get_market_price": get_market_price,
    "calculate_option_price": calculate_option_price,
    "calculate_option_greeks": calculate_option_greeks,
    "calculate_portfolio_risk": calculate_portfolio_risk,
    "get_credit_rating": get_credit_rating,
    "get_alpha_signal": get_alpha_signal,
    "run_backtest": run_backtest,
    "get_user_watchlist": get_user_watchlist,
    "add_ticker_to_watchlist": add_ticker_to_watchlist,
    "get_user_portfolio": get_user_portfolio,
    "add_portfolio_position": add_portfolio_position,
    "link_memories": link_memories,
    "get_related_memories": get_related_memories,
    "get_contextual_memories": get_contextual_memories,
    "optimize_memory_storage": optimize_memory_storage
}

def list_tools():
    return list(TOOLS.keys())

def get_tool(name):
    return TOOLS.get(name)
