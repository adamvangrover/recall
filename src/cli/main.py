import click
from src.llm.main import add_memory, search_memory, list_memories, delete_memory

@click.group()
def cli():
    pass

@cli.command()
@click.argument('memory')
def add(memory):
    """Adds a new memory to the system."""
    if add_memory(memory):
        click.echo(f"Memory added: {memory}")
    else:
        click.echo("Failed to add memory.")

@cli.command()
@click.argument('query')
def search(query):
    """Searches for memories based on a query."""
    results = search_memory(query)
    if results:
        for result in results:
            click.echo(result)
    else:
        click.echo("No results found.")

@cli.command(name="list")
def list_command():
    """Lists all memories."""
    results = list_memories()
    if results:
        for result in results:
            click.echo(result)
    else:
        click.echo("No memories found.")

@cli.command()
@click.argument('id')
def delete(id):
    """Deletes a memory by its ID."""
    if delete_memory(id):
        click.echo(f"Memory with ID {id} deleted.")
    else:
        click.echo(f"Failed to delete memory with ID {id}.")
