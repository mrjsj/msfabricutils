import argparse
import logging
import sys
from typing import Callable

from msfabricutils import __version__
from msfabricutils.cli.lakehouse import create_lakehouse_command, delete_lakehouse_command
from msfabricutils.cli.notebook import (
    bulk_create_notebook_command,
    create_notebook_command,
    delete_notebook_command,
)
from msfabricutils.cli.workspace import create_workspace_command, delete_workspace_command


def create_parser():
    """Creates the main parser and subparsers."""
    examples = """
Examples:
    Create a workspace:
        msfu workspace create --name "My Workspace" --description "My Workspace Description" --capacity-id "beefbeef-beef-beef-beef-beefbeefbeef" --on-conflict "update"
    
    Create a lakehouse:
        msfu lakehouse create --name "My Lakehouse" --description "My Lakehouse Description" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef" --on-conflict "update"
    
    Create a single notebook:
        msfu notebook create --path "path/to/notebook.Notebook" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef"

    Create multiple notebooks:
        msfu notebook create --path "directory/of/notebooks" "path/to/notebook.Notebook" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef"
    """

    parser = argparse.ArgumentParser(
        prog="msfabricutils",
        description="Utility CLI for Microsoft Fabric REST API operations",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", "-v", action="version", version=__version__)
    parser.add_argument(
        "--log-level",
        "-l",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="The log level to use. Defaults to INFO.",
    )
    parser.add_argument(
        "--show-azure-identity-logs",
        action="store_true",
        default=False,
        help="Show Azure Identity logs. Defaults to False.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    register_workspace_commands(subparsers)
    register_lakehouse_commands(subparsers)
    register_notebook_commands(subparsers)

    return parser


def register_workspace_commands(subparsers: argparse._SubParsersAction):
    """Registers the workspace commands."""
    workspace_parser = subparsers.add_parser("workspace", help="Workspace commands")
    workspace_subparsers = workspace_parser.add_subparsers(
        dest="workspace", help="Workspace commands"
    )
    add_subcommand(
        subparsers=workspace_subparsers,
        name="create",
        handler=create_workspace_command,
        required_args=["--name"],
        choices_args={"--on-conflict": ["error", "ignore", "update"]},
        optional_args=["--description", "--capacity-id"],
    )
    add_subcommand(
        subparsers=workspace_subparsers,
        name="delete",
        handler=delete_workspace_command,
        mutually_exclusive_args=["--id", "--name"],
        choices_args={"--on-conflict": ["error", "ignore"]},
    )


def register_lakehouse_commands(subparsers: argparse._SubParsersAction):
    """Registers the lakehouse commands."""
    lakehouse_parser = subparsers.add_parser("lakehouse", help="Lakehouse commands")
    lakehouse_subparsers = lakehouse_parser.add_subparsers(
        dest="lakehouse", help="Lakehouse commands"
    )

    add_subcommand(
        subparsers=lakehouse_subparsers,
        name="create",
        handler=create_lakehouse_command,
        required_args=["--name", "--workspace-id"],
        has_long_running_operation=True,
        choices_args={
            "--on-conflict": ["error", "ignore", "update"],
        },
        optional_args=["--description"],
        flags=["--enable-schemas"],
    )
    add_subcommand(
        subparsers=lakehouse_subparsers,
        name="delete",
        handler=delete_lakehouse_command,
        required_args=["--workspace-id"],
        mutually_exclusive_args=["--id", "--name"],
        choices_args={"--on-conflict": ["error", "ignore"]},
    )


def register_notebook_commands(subparsers: argparse._SubParsersAction):
    """Registers the notebook commands."""
    notebook_parser = subparsers.add_parser("notebook", help="Notebook commands")
    notebook_subparsers = notebook_parser.add_subparsers(dest="notebook", help="Notebook commands")
    
    add_subcommand(
        subparsers=notebook_subparsers,
        name="create",
        handler=create_notebook_command,
        required_args=["--workspace-id", "--path"],
        optional_args=["--name", "--description"],
        has_long_running_operation=True,
        choices_args={"--on-conflict": ["error", "ignore", "update"]},
    )
    add_subcommand(
        subparsers=notebook_subparsers,
        name="bulk-create",
        handler=bulk_create_notebook_command,
        required_args=["--workspace-id"],
        nargs=["--path"],
        has_long_running_operation=True,
        choices_args={"--on-conflict": ["error", "ignore", "update"]},
    )
    add_subcommand(
        subparsers=notebook_subparsers,
        name="delete",
        handler=delete_notebook_command,
        required_args=["--workspace-id"],
        mutually_exclusive_args=["--id", "--name"],
        choices_args={"--on-conflict": ["error", "ignore"]},
    )


def add_subcommand(
    subparsers: argparse._SubParsersAction,
    name: str,
    handler: Callable,
    required_args: list[str] | None = None,
    nargs: list[str] | None = None,
    choices_args: dict[str, list[str]] | None = None,
    mutually_exclusive_args: list[str] | None = None,
    optional_args: list[str] | None = None,
    has_long_running_operation: bool = False,
    flags: list[str] | None = None,
):
    """Adds a subcommand to the parser.

    Args:
        subparsers (argparse._SubParsersAction): The subparsers to add the subcommand to.
        name (str): The name of the subcommand.
        handler (Callable): The handler function to call when the subcommand is invoked.
        required_args (list[str] | None): The required arguments for the subcommand.
        nargs (list[str] | None): The nargs arguments for the subcommand.
        choices_args (dict[str, list[str]] | None): The choices arguments for the subcommand. The default choice is the first in the list.
        optional_args (list[str] | None): The optional arguments for the subcommand.
    """

    if not required_args:
        required_args = []

    if not choices_args:
        choices_args = {}

    if not optional_args:
        optional_args = []

    if not nargs:
        nargs = []

    if not flags:
        flags = []

    create_parser = subparsers.add_parser(name, help=f"{name.capitalize()} commands")

    for arg in required_args:
        create_parser.add_argument(
            arg, required=True, help=f"The {arg.lstrip('-')} of the {subparsers.dest} to {name}."
        )

    for arg in nargs:
        create_parser.add_argument(
            arg, nargs="+", help=f"The {arg.lstrip('-')} of the {subparsers.dest}s to {name}."
        )

    for arg in optional_args:
        create_parser.add_argument(
            arg, required=False, help=f"The {arg.lstrip('-')} of the {subparsers.dest} to {name}."
        )

    for flag in flags:
        create_parser.add_argument(
            flag, action="store_true", default=False, help=f"{flag.lstrip('-')} flag for the {subparsers.dest} to {name}."
        )

    if has_long_running_operation:
        create_parser.add_argument(
            "--no-wait", action="store_true", default=False, help="Do not wait for the long running operation to complete."
        )

    if mutually_exclusive_args:
        argument_group = create_parser.add_mutually_exclusive_group(required=True)
        for arg in mutually_exclusive_args:
            argument_group.add_argument(
                arg, help=f"The {arg.lstrip('-')} of the {subparsers.dest} to {name}."
            )

    for arg, choices in choices_args.items():
        create_parser.add_argument(
            arg,
            type=str,
            choices=choices,
            default=choices[0],
            help=f"The {arg.lstrip('-')} of the {subparsers.dest} to {name}. Defaults to `{choices[0]}`.",
        )

    create_parser.set_defaults(func=handler)


def main():
    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    )

    try:
        azure_log_level = args.log_level if args.show_azure_identity_logs else logging.CRITICAL
        logging.getLogger("azure").setLevel(azure_log_level)
        args.func(args)
    except Exception as e:
        logging.error(e)
        sys.stderr.write(str(e))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
