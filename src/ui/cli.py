import click
import uvicorn
import os
from src.core.services import add_memory, search_memory, list_memories, delete_memory
from src.core.ingestion import IngestionService
from src.memory.vector_store import VectorMemoryStore

@click.group()
def cli():
    """Total Recall: A portable, LLM-powered personal recall system."""
    pass

@cli.command()
@click.argument('content')
def add(content):
    """Adds a new memory to the system."""
    memory_id = add_memory(content)
    if memory_id:
        click.echo(f"Memory added with ID: {memory_id}")
    else:
        click.echo("Failed to add memory.")

@cli.command()
@click.argument('query')
def search(query):
    """Performs a semantic search for memories."""
    results = search_memory(query)
    if results:
        click.echo("Found memories:")
        for res in results:
            similarity = res.get('similarity', 0) * 100
            click.echo(f"- ID: {res['id']}, Similarity: {similarity:.2f}%\n  Content: {res['content']}\n")
    else:
        click.echo("No results found.")

@cli.command(name="list")
def list_command():
    """Lists all memories."""
    results = list_memories()
    if results:
        click.echo("All memories:")
        for res in results:
            click.echo(f"- ID: {res['id']}\n  Content: {res['content']}\n")
    else:
        click.echo("No memories found.")

@cli.command()
@click.argument('memory_id')
def delete(memory_id):
    """Deletes a memory by its ID."""
    if delete_memory(memory_id):
        click.echo(f"Memory with ID {memory_id} deleted.")
    else:
        # This branch may not be hit if ChromaDB doesn't error, but it's good practice.
        click.echo(f"Failed to delete memory with ID {memory_id}.")

@cli.command()
@click.argument('path')
def ingest(path):
    """Ingests text/markdown files from a directory."""
    click.echo(f"Ingesting files from: {path}")
    store = VectorMemoryStore()
    service = IngestionService(store)
    count = service.ingest_directory(path)
    click.echo(f"Successfully ingested {count} files.")

@cli.command()
@click.option('--port', default=8000, help='Port to run the API on.')
def serve(port):
    """Starts the Agent API server."""
    click.echo(f"Starting API server on port {port}...")
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=port, reload=False)

@cli.group(name="recall", invoke_without_command=True)
@click.pass_context
def recall_group(ctx):
    """Advanced recall features."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@recall_group.command(name="graph")
@click.argument('memory_id')
def graph_cmd(memory_id):
    """Visualizes the connections for a specific memory."""
    from src.core.services import get_memory_graph
    result = get_memory_graph(memory_id)
    click.echo(result)

@recall_group.command(name="link")
@click.argument('source_id')
@click.argument('target_id')
@click.option('--relation', default="related_to", help='Relationship type')
def link_cmd(source_id, target_id, relation):
    """Explicitly link two memories in the Knowledge Graph."""
    from src.core.services import link_memories
    if link_memories(source_id, target_id, relation):
        click.echo(f"Successfully linked {source_id} -> {target_id} [{relation}]")
    else:
        click.echo("Failed to link memories.")

@recall_group.command(name="optimize")
@click.option('--days', default=30, help='Number of days inactive to consider cold')
def optimize_cmd(days):
    """Scans for cold memories and calculates potential storage savings."""
    from src.core.services import optimize_memory_storage
    results = optimize_memory_storage(days)
    click.echo(f"Optimization Analysis (Inactive > {days} days):")
    click.echo(f"Cold Memories Found: {results['cold_count']}")
    click.echo(f"Total Original Size (Cold): {results['total_original_bytes']} bytes")
    click.echo(f"Total Compressed Size (Cold): {results['total_compressed_bytes']} bytes")
    click.echo(f"Potential Storage Savings: {results['potential_savings_bytes']} bytes")
