import click
import uvicorn
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.core.services import add_memory, search_memory, list_memories, delete_memory
from src.core.ingestion import IngestionService
from src.memory.vector_store import VectorMemoryStore

console = Console()

@click.group()
def cli():
    """Total Recall: A portable, LLM-powered personal recall system."""
    pass

def prompt_if_missing(ctx, param, value):
    if not value:
        return click.prompt(f"Please provide {param.name}")
    return value

@cli.command()
@click.argument('content', callback=prompt_if_missing, required=False)
def add(content):
    """Adds a new memory to the system."""
    memory_id = add_memory(content)
    if memory_id:
        console.print(f"[bold green]Memory added successfully![/bold green] (ID: [cyan]{memory_id}[/cyan])")
    else:
        console.print("[bold red]Failed to add memory.[/bold red]")

@cli.command()
@click.argument('query', callback=prompt_if_missing, required=False)
def search(query):
    """Performs a semantic search for memories."""
    results = search_memory(query)
    if results:
        table = Table(title=f"Search Results for '{query}'", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Similarity", justify="right", style="green")
        table.add_column("Content")

        for res in results:
            similarity = res.get('similarity', 0) * 100
            table.add_row(res['id'], f"{similarity:.2f}%", res['content'])

        console.print(table)
    else:
        console.print("[yellow]No memories found matching your query.[/yellow]")

@cli.command(name="list")
def list_command():
    """Lists all memories."""
    results = list_memories()
    if results:
        table = Table(title="All Memories", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Content")

        for res in results:
            table.add_row(res['id'], res['content'])

        console.print(table)
    else:
        console.print("[yellow]No memories found in the system.[/yellow]")

@cli.command()
@click.argument('memory_id', callback=prompt_if_missing, required=False)
def delete(memory_id):
    """Deletes a memory by its ID."""
    if delete_memory(memory_id):
        console.print(f"[bold green]Successfully deleted memory ID:[/bold green] [cyan]{memory_id}[/cyan]")
    else:
        # This branch may not be hit if ChromaDB doesn't error, but it's good practice.
        console.print(f"[bold red]Failed to delete memory with ID {memory_id}.[/bold red]")

@cli.command()
@click.argument('path', callback=prompt_if_missing, required=False)
def ingest(path):
    """Ingests text/markdown files from a directory."""
    console.print(f"Ingesting files from: [cyan]{path}[/cyan]...")
    store = VectorMemoryStore()
    service = IngestionService(store)
    count = service.ingest_directory(path)
    console.print(f"[bold green]Successfully ingested {count} files.[/bold green]")

@cli.command()
@click.option('--port', default=8000, help='Port to run the API on.')
def serve(port):
    """Starts the Agent API server."""
    console.print(f"[bold green]Starting API server on port {port}...[/bold green]")
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=port, reload=False)

@cli.group(name="recall", invoke_without_command=True)
@click.pass_context
def recall_group(ctx):
    """Advanced recall features."""
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())

@recall_group.command(name="graph")
@click.argument('memory_id', callback=prompt_if_missing, required=False)
def graph_cmd(memory_id):
    """Visualizes the connections for a specific memory."""
    from src.core.services import get_memory_graph
    result = get_memory_graph(memory_id)
    panel = Panel(result, title=f"Knowledge Graph: [cyan]{memory_id}[/cyan]", border_style="blue")
    console.print(panel)

@recall_group.command(name="link")
@click.argument('source_id', callback=prompt_if_missing, required=False)
@click.argument('target_id', callback=prompt_if_missing, required=False)
@click.option('--relation', default="related_to", help='Relationship type')
def link_cmd(source_id, target_id, relation):
    """Explicitly link two memories in the Knowledge Graph."""
    from src.core.services import link_memories
    if link_memories(source_id, target_id, relation):
        console.print(f"[bold green]Successfully linked[/bold green] [cyan]{source_id}[/cyan] -> [cyan]{target_id}[/cyan] [[magenta]{relation}[/magenta]]")
    else:
        console.print("[bold red]Failed to link memories.[/bold red]")

@recall_group.command(name="optimize")
@click.option('--days', default=30, help='Number of days inactive to consider cold')
def optimize_cmd(days):
    """Scans for cold memories and calculates potential storage savings."""
    from src.core.services import optimize_memory_storage
    results = optimize_memory_storage(days)

    content = (
        f"[bold]Cold Memories Found:[/bold] {results['cold_count']}\n"
        f"[bold]Total Original Size (Cold):[/bold] {results['total_original_bytes']} bytes\n"
        f"[bold]Total Compressed Size (Cold):[/bold] {results['total_compressed_bytes']} bytes\n"
        f"\n"
        f"[bold green]Potential Storage Savings:[/bold green] {results['potential_savings_bytes']} bytes"
    )

    panel = Panel(content, title=f"Optimization Analysis (Inactive > {days} days)", border_style="green")
    console.print(panel)
