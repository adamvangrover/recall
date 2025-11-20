import click
from src.llm.services import add_memory, search_memory, list_memories, delete_memory

@click.group()
def cli():
    """A portable, LLM-powered personal recall system."""
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
