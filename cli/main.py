from cyclopts import App
# from rich.console import Console
from rich.tree import Tree
from typing import Annotated, List
from cyclopts import Parameter

from console import console


def show_command_tree(commands: Annotated[List[str], Parameter(help="Space delimited list of commands to filter the command tree by. Example: `msfu tree lakehouse`, `msfu tree lakehouse tables`.", consume_multiple=True)] = None) -> None:
    """Display the complete command tree structure.
    
    Args:
        commands (str): Space delimited list of commands to filter the command tree by.

    """
    global _app
    
    tree = Tree("CLI Commands")
    
    def add_commands_to_tree(commands, tree_node, subcommands):
        filter_cmd = None
        filter_args = None
        if subcommands:
            # subcommands = subcommand.split(" ")
            filter_cmd = subcommands[0]
            filter_args = subcommands[1:]

        for name, cmd in commands.items():
            if filter_cmd and name != filter_cmd:
                continue
            if name in ("--help", "--version", "-h"):
                continue
            cmd_node = tree_node.add(name)
            if hasattr(cmd, '_commands') and cmd._commands:
                add_commands_to_tree(cmd._commands, cmd_node, filter_args)
    
    add_commands_to_tree(_app._commands, tree, commands)
    console.print(tree, markup=True)



def create_app() -> App:
    from commands.admin import admin_app
    from commands.core import core_app
    # Add the auth command
    help_message = """[bold green]Welcome to the msfabricutils CLI[/bold green]\n :exclamation:Currently under development - use with caution
    
Authentication is handled by the `msfabricpysdkcore` package. See: [link=https://pypi.org/project/msfabricpysdkcore]https://pypi.org/project/msfabricpysdkcore[/link]

In short the following authentication methods are supported:
- Azure CLI - (e.g. run `az login`)
- Service Principal Authentication - by setting the environment variables: [bold]FABRIC_CLIENT_ID[/bold], [bold]FABRIC_CLIENT_SECRET[/bold], and [bold]FABRIC_TENANT_ID[/bold]
- MSALConfidentialClientApplicationAuthentication - by setting the environment variables: [bold]FABRIC_USERNAME[/bold], [bold]FABRIC_PASSWORD[/bold], and [bold]FABRIC_TENANT_ID[/bold]
    """
    global _app
    _app = App(help=help_message, help_format="rich")

    _app.command(admin_app)
    _app._commands = (
        _app._commands |
        core_app._commands
    )
    
    # Add the tree command
    _app.command(show_command_tree, name="tree")


    return _app


def main():
    from rich.status import Status
    with Status("Running ...", spinner="bouncingBall", console=console):
        app = create_app()
        app()


if __name__ == "__main__":
    main()


