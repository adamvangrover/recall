import click
import json
import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import print as rprint
from rich.tree import Tree

from memory.sync_interface.services import add_memory, search_memory, list_memories, delete_memory
from mcp.tools import (
    get_market_price, calculate_option_price, calculate_option_greeks,
    calculate_portfolio_risk, get_credit_rating, get_alpha_signal,
    run_backtest, get_user_watchlist, add_ticker_to_watchlist,
    get_user_portfolio, add_portfolio_position,
    link_memories, get_related_memories, get_contextual_memories,
    optimize_memory_storage
)

console = Console()

@click.group()
def cli():
    """FO Super-App: Markets, Pricing, Ratings, Execution, Analytics & Memory."""
    pass

# --- Dashboard ---
@cli.command()
def dashboard():
    """Show the FO Morning Briefing."""
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=5)
    )

    layout["header"].update(Panel("FO Super-App: Morning Briefing", style="bold white on blue"))

    # Left: Watchlist & Signals
    watchlist = get_user_watchlist()
    wl_table = Table(title="Watchlist Monitor", expand=True)
    wl_table.add_column("Ticker", style="cyan")
    wl_table.add_column("Price", justify="right")
    wl_table.add_column("Signal", justify="center")

    if not watchlist:
        wl_table.add_row("-", "-", "No tickers")
    else:
        for ticker in watchlist:
            price = get_market_price(ticker)
            sig = get_alpha_signal(ticker)
            signal_color = "green" if sig['signal'] == 'BUY' else "red" if sig['signal'] == 'SELL' else "yellow"
            wl_table.add_row(ticker, f"${price:.2f}", f"[{signal_color}]{sig['signal']}[/{signal_color}]")

    # Right: Portfolio Risk
    portfolio = get_user_portfolio()

    # Calculate Risk
    risk_portfolio = []
    total_val = 0
    if portfolio:
        for p in portfolio:
            current_price = get_market_price(p['symbol'])
            val = p['quantity'] * current_price
            risk_portfolio.append({'symbol': p['symbol'], 'value': val})
            total_val += val

        metrics = calculate_portfolio_risk(risk_portfolio)
        status_color = "red" if metrics['status'] == 'Breach' else "green"

        risk_text = (
            f"[bold]Total Value:[/bold] ${metrics['total_value']:,.2f}\n"
            f"[bold]VaR (95%):[/bold] [red]${metrics['VaR_95']:,.2f}[/red]\n"
            f"[bold]VaR (99%):[/bold] [bold red]${metrics['VaR_99']:,.2f}[/bold red]\n"
            f"[bold]Status:[/bold] [{status_color}]{metrics['status']}[/{status_color}]"
        )
    else:
        risk_text = "No portfolio data."
        status_color = "white"

    risk_panel = Panel(
        risk_text,
        title="Portfolio Risk",
        border_style=status_color
    )

    layout["main"].split_row(
        Layout(wl_table, name="left"),
        Layout(risk_panel, name="right")
    )

    # Footer: Contextual Memories (What's relevant now?)
    # For demo, use "market" as context
    context_mems = get_contextual_memories("market finance strategy")
    mem_text = ""
    if context_mems:
        for m in context_mems[:3]:
            score = m.get('recall_score', 0)
            mem_text += f"[{score:.2f}] {m['content'][:80]}...\n"
    else:
        mem_text = "No relevant context found."

    layout["footer"].update(Panel(mem_text, title="Contextual Recall (Market)", border_style="blue"))

    console.print(layout)


# --- Memory Commands ---
@cli.group()
def memory():
    """Personal Sandbox Memory commands."""
    pass

@memory.command()
@click.argument('content')
def add(content):
    """Adds a new memory to the system."""
    memory_id = add_memory(content)
    if memory_id:
        console.print(f"[green]Memory added with ID: {memory_id}[/green]")
    else:
        console.print("[red]Failed to add memory.[/red]")

@memory.command()
@click.argument('query')
def search(query):
    """Performs a semantic search for memories."""
    results = search_memory(query)
    if results:
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Score", justify="right")
        table.add_column("Content")
        table.add_column("Tags", style="magenta")

        for res in results:
            similarity = res.get('similarity', 0) * 100
            meta = res.get('metadata', {}) or {}
            tags = meta.get('tags', "")
            table.add_row(res['id'][:8], f"{similarity:.1f}%", res['content'], tags)
        console.print(table)
    else:
        console.print("[yellow]No results found.[/yellow]")

@memory.command(name="list")
def list_command():
    """Lists all memories."""
    results = list_memories()
    if results:
        table = Table(title="All Memories")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Content")
        table.add_column("Summary", style="dim")
        table.add_column("Tags", style="magenta")

        for res in results:
            meta = res.get('metadata', {}) or {}
            summary = meta.get('summary', "")[:50]
            tags = meta.get('tags', "")
            table.add_row(res['id'][:8], res['content'], summary, tags)
        console.print(table)
    else:
        console.print("[yellow]No memories found.[/yellow]")

@memory.command()
@click.argument('memory_id')
def delete(memory_id):
    """Deletes a memory by its ID."""
    if delete_memory(memory_id):
        console.print(f"[green]Memory {memory_id} deleted.[/green]")
    else:
        console.print(f"[red]Failed to delete memory {memory_id}.[/red]")

@memory.command()
@click.argument('id1')
@click.argument('id2')
@click.option('--relation', default='related', help='Relationship type')
def link(id1, id2, relation):
    """Link two memories."""
    msg = link_memories(id1, id2, relation)
    console.print(f"[green]{msg}[/green]")

@memory.command()
@click.argument('memory_id')
def graph(memory_id):
    """Visualize memory connections."""
    related = get_related_memories(memory_id)
    if not related:
        console.print("[yellow]No related memories found.[/yellow]")
        return

    tree = Tree(f"[bold]{memory_id}[/bold]")
    for r in related:
        tree.add(f"[cyan]{r}[/cyan]")

    console.print(tree)

@memory.command()
@click.argument('context')
def recall(context):
    """Context-aware recall."""
    results = get_contextual_memories(context)
    if results:
        table = Table(title=f"Recall Context: {context}")
        table.add_column("ID", style="dim")
        table.add_column("Recall Score", justify="right", style="bold green")
        table.add_column("Content")

        for res in results:
            table.add_row(res['id'][:8], f"{res['recall_score']:.2f}", res['content'])
        console.print(table)
    else:
        console.print("[yellow]No relevant memories found.[/yellow]")

@memory.command()
def optimize():
    """Run memory optimization."""
    stats = optimize_memory_storage()

    panel = Panel(
        f"Total Memories: {stats['total_memories']}\n"
        f"Original Size: {stats['total_size_original']} bytes\n"
        f"Compressed Size: {stats['total_size_compressed']} bytes\n"
        f"Savings: [green]{stats['space_saved']} bytes[/green] (Ratio: {stats['compression_ratio']})\n\n"
        f"Cold Memories: {stats['cold_memories_count']} ({stats['cold_memories_size']} bytes)\n"
        f"Recommendation: [bold]{stats['recommendation']}[/bold]",
        title="Memory Optimization Report"
    )
    console.print(panel)

# --- Profile Commands ---
@cli.group()
def profile():
    """Manage user profile (Watchlist, Portfolio)."""
    pass

@profile.command(name="watch")
@click.argument('ticker')
def watchlist_add(ticker):
    """Add ticker to watchlist."""
    msg = add_ticker_to_watchlist(ticker)
    console.print(f"[green]{msg}[/green]")

@profile.command(name="buy")
@click.argument('symbol')
@click.argument('qty', type=float)
@click.argument('price', type=float)
def portfolio_add(symbol, qty, price):
    """Add position (Buy). usage: buy SYMBOL QTY PRICE"""
    msg = add_portfolio_position(symbol, qty, price)
    console.print(f"[green]{msg}[/green]")

@profile.command(name="show")
def profile_show():
    """Show full profile."""
    # Watchlist
    wl = get_user_watchlist()
    console.print(Panel(f"Watchlist: {', '.join(wl)}", title="Watchlist"))

    # Portfolio
    pf = get_user_portfolio()
    if not pf:
        console.print("[yellow]Portfolio is empty.[/yellow]")
    else:
        table = Table(title="Portfolio")
        table.add_column("Symbol")
        table.add_column("Qty", justify="right")
        table.add_column("Avg Price", justify="right")
        table.add_column("Current Price", justify="right")
        table.add_column("P&L", justify="right")

        total_pnl = 0
        for p in pf:
            curr = get_market_price(p['symbol'])
            cost = p['quantity'] * p['avg_price']
            val = p['quantity'] * curr
            pnl = val - cost
            pnl_color = "green" if pnl >= 0 else "red"
            total_pnl += pnl

            table.add_row(
                p['symbol'],
                f"{p['quantity']}",
                f"${p['avg_price']:.2f}",
                f"${curr:.2f}",
                f"[{pnl_color}]${pnl:.2f}[/{pnl_color}]"
            )
        console.print(table)
        pnl_color = "green" if total_pnl >= 0 else "red"
        console.print(f"Total P&L: [{pnl_color} bold]${total_pnl:.2f}[/{pnl_color} bold]")


# --- Market Data ---
@cli.command()
@click.argument('ticker')
def price(ticker):
    """Get current market price for a ticker."""
    p = get_market_price(ticker)
    console.print(Panel(f"{ticker}: [bold green]${p}[/bold green]", title="Market Data"))

# --- Ratings ---
@cli.command()
@click.argument('entity')
def rate(entity):
    """Get credit rating for an entity."""
    r = get_credit_rating(entity)
    color = "green" if 'A' in r['rating'] else "yellow" if 'B' in r['rating'] else "red"
    console.print(Panel(
        f"Rating: [{color}]{r['rating']}[/{color}]\nOutlook: {r['outlook']}\nDate: {r['date']}",
        title=f"Credit Rating: {entity}"
    ))

# --- Risk ---
@cli.command()
@click.argument('portfolio_json', required=False)
def risk(portfolio_json):
    """Calculate risk metrics for a portfolio (JSON string)."""
    if not portfolio_json:
        # Use profile portfolio if available, else demo
        pf = get_user_portfolio()
        if pf:
            portfolio = []
            for p in pf:
                # Convert
                 val = p['quantity'] * get_market_price(p['symbol'])
                 portfolio.append({'symbol': p['symbol'], 'value': val})
            console.print("[dim]Using User Portfolio[/dim]")
        else:
            portfolio = [{'symbol': 'AAPL', 'value': 15000}, {'symbol': 'GOOG', 'value': 20000}]
            console.print("[dim]Using Demo Portfolio[/dim]")
    else:
        try:
            portfolio = json.loads(portfolio_json)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON string.[/red]")
            return

    metrics = calculate_portfolio_risk(portfolio)

    table = Table(title="Risk Metrics")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Total Value", f"${metrics['total_value']:,.2f}")
    table.add_row("VaR (95%)", f"[red]${metrics['VaR_95']:,.2f}[/red]")
    table.add_row("VaR (99%)", f"[bold red]${metrics['VaR_99']:,.2f}[/bold red]")
    table.add_row("Status", metrics['status'])

    console.print(table)

# --- Signal ---
@cli.command()
@click.argument('ticker')
def signal(ticker):
    """Generate alpha signal for a ticker."""
    sig = get_alpha_signal(ticker)

    color = "green" if sig['signal'] == 'BUY' else "red" if sig['signal'] == 'SELL' else "yellow"

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row("Signal:", f"[{color} bold]{sig['signal']}[/{color bold}]")
    grid.add_row("Confidence:", f"{sig['confidence']:.2f}")
    grid.add_row("Current Price:", f"${sig['current_price']:.2f}")
    grid.add_row("SMA (5):", f"{sig['sma_5']:.2f}")
    grid.add_row("SMA (20):", f"{sig['sma_20']:.2f}")

    console.print(Panel(grid, title=f"Alpha Signal: {ticker}"))

# --- Pricing ---
@cli.command()
@click.option('--s', type=float, required=True, help='Spot Price')
@click.option('--k', type=float, required=True, help='Strike Price')
@click.option('--t', type=float, required=True, help='Time to Maturity (years)')
@click.option('--r', type=float, default=0.05, help='Risk-free Rate')
@click.option('--sigma', type=float, default=0.2, help='Volatility')
@click.option('--type', 'option_type', type=click.Choice(['call', 'put']), default='call', help='Option Type')
def option(s, k, t, r, sigma, option_type):
    """Calculate Option Price & Greeks (Black-Scholes)."""
    price = calculate_option_price(s, k, t, r, sigma, option_type)
    greeks = calculate_option_greeks(s, k, t, r, sigma, option_type)

    table = Table(title=f"{option_type.capitalize()} Option Analysis")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Price", f"[bold green]${price:.4f}[/bold green]")
    table.add_row("Delta", f"{greeks['delta']:.4f}")
    table.add_row("Gamma", f"{greeks['gamma']:.4f}")
    table.add_row("Theta", f"{greeks['theta']:.4f}")
    table.add_row("Vega", f"{greeks['vega']:.4f}")
    table.add_row("Rho", f"{greeks['rho']:.4f}")

    console.print(table)

# --- Backtest ---
@cli.command()
@click.argument('ticker')
@click.option('--days', default=365, help='Days to backtest')
@click.option('--capital', default=100000.0, help='Initial Capital')
def backtest(ticker, days, capital):
    """Run a backtest simulation."""
    with console.status(f"[bold green]Running backtest for {ticker}...[/bold green]"):
        res = run_backtest(ticker, days, capital)

    console.print(Panel(f"Backtest Complete: {ticker}", style="bold white on blue"))

    # Summary Table
    sum_table = Table(title="Performance Summary")
    sum_table.add_column("Metric")
    sum_table.add_column("Value", justify="right")

    sum_table.add_row("Total Return", f"[bold]{res['total_return_pct']}%[/bold]")
    sum_table.add_row("Final Value", f"${res['final_value']:,.2f}")
    sum_table.add_row("Sharpe Ratio", f"{res['sharpe_ratio']:.2f}")
    sum_table.add_row("Max Drawdown", f"[red]{res['max_drawdown_pct']}%[/red]")
    sum_table.add_row("Trades Executed", str(res['trades_count']))

    console.print(sum_table)

if __name__ == '__main__':
    cli()
