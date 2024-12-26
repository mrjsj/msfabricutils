import logging
from importlib.metadata import PackageNotFoundError, version

import typer
from typing_extensions import Annotated

from msfabricutils.cli.commands import COMMANDS

app = typer.Typer(
    name="msfabricutils",
    help="""[bold red]Authentication:[/bold red]
This tool uses automatic authentication.
You must be logged in to Azure (e.g., via 'az login') before using this tool.
[bold yellow]Important:[/bold yellow]
This tool is in active development. The commands and subcommands are subject to change.
""",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def version_callback(value: bool):
    if value:
        try:
            ver = version("msfabricutils")
        except PackageNotFoundError:
            ver = "0.0.0"
        typer.echo(f"msfabricutils: v{ver}")
        raise typer.Exit()


@app.callback()
def common_options(
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show version and exit", callback=version_callback),
    ] = False,
):
    pass


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("azure").setLevel(logging.CRITICAL)

    for command, sub_app in COMMANDS.items():
        app.add_typer(sub_app, name=command)
    app()


if __name__ == "__main__":
    main()
