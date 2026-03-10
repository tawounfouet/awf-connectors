import typer
from rich.console import Console
from rich.table import Table

from pyconnectors.registry import ConnectorRegistry

app = typer.Typer()
console = Console()

# We need to import the connectors so they are registered
# In a real app we might load them dynamically or have an entry point based plugin system
# For now, let's just make sure the subpackages are imported
import pyconnectors.connectors.database.mongodb  # noqa
import pyconnectors.connectors.database.mysql  # noqa
import pyconnectors.connectors.database.postgresql  # noqa
import pyconnectors.connectors.database.redis  # noqa
import pyconnectors.connectors.database.sqlite  # noqa
import pyconnectors.connectors.email.smtp  # noqa
import pyconnectors.connectors.http.rest  # noqa
import pyconnectors.connectors.social.facebook  # noqa
import pyconnectors.connectors.social.instagram  # noqa
import pyconnectors.connectors.social.linkedin  # noqa
import pyconnectors.connectors.social.slack  # noqa
import pyconnectors.connectors.social.tiktok  # noqa
import pyconnectors.connectors.social.twitter  # noqa
import pyconnectors.connectors.social.whatsapp  # noqa
import pyconnectors.connectors.storage.s3  # noqa


@app.callback(invoke_without_command=True)
def main() -> None:
    """List all available connectors."""
    connectors = ConnectorRegistry.list_connectors()

    if not connectors:
        console.print("[yellow]No connectors found.[/yellow]")
        return

    table = Table(title="Available Connectors")
    table.add_column("Name", style="cyan")
    table.add_column("Class", style="magenta")

    for name, cls in sorted(connectors.items()):
        table.add_row(name, cls.__name__)

    console.print(table)
