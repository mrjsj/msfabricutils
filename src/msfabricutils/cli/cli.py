import argparse
import json
import logging
import sys

from msfabricutils import __version__
from msfabricutils.cli.workspace import create_workspace_command, delete_workspace_command


def main():
    examples = """
Examples:
    Create a workspace:
        msfu workspace create --name "My Workspace" --description "My Workspace Description" --capacity-id "beefbeef-beef-beef-beef-beefbeefbeef" --on-conflict "update"
    
    Create a lakehouse:
        msfu lakehouse create --name "My Lakehouse" --description "My Lakehouse Description" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef" --on-conflict "update"
    
    Create a single notebook:
        msfu notebook create --path "path/to/myNotebook.Notebook" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef"

    Create multiple notebooks:
        msfu notebook create --path "path/to/notebooks" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef"
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

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subcommand: workspace
    workspace_parser = subparsers.add_parser("workspace", help="Workspace commands")
    workspace_subparsers = workspace_parser.add_subparsers(
        dest="workspace_command", help="Workspace commands"
    )

    # Subcommand: workspace create
    workspace_create_parser = workspace_subparsers.add_parser("create", help="Create a workspace")
    workspace_create_parser.add_argument(
        "--name", "-n", type=str, required=True, help="The name of the workspace."
    )
    workspace_create_parser.add_argument(
        "--description", "-d", type=str, help="The description of the workspace."
    )
    workspace_create_parser.add_argument(
        "--capacity-id", "-c", type=str, help="The Fabric capacity id to assign the workspace to."
    )
    workspace_create_parser.add_argument(
        "--on-conflict",
        type=str,
        choices=["ignore", "update", "error"],
        default="error",
        help="The action to take if the workspace already exists. Defaults to `error`.",
    )

    # Subcommand: workspace delete
    workspace_delete_parser = workspace_subparsers.add_parser("delete", help="Delete a workspace")
    workspace_delete_group = workspace_delete_parser.add_mutually_exclusive_group(required=True)
    workspace_delete_group.add_argument(
        "--id", "-i", type=str, help="The ID of the workspace to delete."
    )
    workspace_delete_group.add_argument(
        "--name", "-n", type=str, help="The name of the workspace to delete."
    )
    workspace_delete_parser.add_argument(
        "--on-conflict",
        type=str,
        choices=["ignore", "error"],
        default="error",
        help="The action to take if the workspace does not exist. Defaults to `error`.",
    )

    # Subcommand: lakehouse
    lakehouse_parser = subparsers.add_parser("lakehouse", help="Lakehouse commands")
    lakehouse_subparsers = lakehouse_parser.add_subparsers(
        dest="lakehouse_command", help="Lakehouse commands"
    )

    # Subcommand: lakehouse create
    lakehouse_create_parser = lakehouse_subparsers.add_parser("create", help="Create a lakehouse")
    lakehouse_create_parser.add_argument(
        "--name", "-n", type=str, required=True, help="The name of the lakehouse."
    )
    lakehouse_create_parser.add_argument(
        "--description", "-d", type=str, help="The description of the lakehouse."
    )
    lakehouse_create_parser.add_argument(
        "--workspace-id",
        "-w",
        type=str,
        required=True,
        help="The workspace id to create the lakehouse in.",
    )
    lakehouse_create_parser.add_argument(
        "--on-conflict",
        type=str,
        choices=["ignore", "update", "error"],
        default="error",
        help="The action to take if the lakehouse already exists. Defaults to `error`.",
    )

    # Subcommand: notebook
    notebook_parser = subparsers.add_parser("notebook", help="Notebook commands")
    notebook_subparsers = notebook_parser.add_subparsers(
        dest="notebook_command", help="Notebook commands"
    )

    notebook_create_parser = notebook_subparsers.add_parser("create", help="Create a notebook")
    notebook_create_parser.add_argument(
        "--path",
        "-p",
        type=str,
        required=True,
        help="Path to folder of notebooks or a single notebook to publish. Single notebook should end with `.Notebook`.",
    )
    notebook_create_parser.add_argument(
        "--workspace-id",
        "-w",
        type=str,
        required=True,
        help="The workspace id to publish the notebook to.",
    )
    notebook_create_parser.add_argument(
        "--name",
        "-n",
        type=str,
        help="The name of the notebook. If not provided, the name of the notebook file will be used.",
    )
    notebook_create_parser.add_argument(
        "--description",
        "-d",
        type=str,
        help="The description of the notebook. Only applicable if publishing a single notebook.",
    )
    notebook_create_parser.add_argument(
        "--on-conflict",
        type=str,
        choices=["ignore", "update", "error"],
        default="error",
        help="The action to take if the notebook already exists. Defaults to `error`.",
    )

    args = parser.parse_args()

    # Format as json
    logging.basicConfig(
        level=args.log_level,
        format='{"timestamp": "%(asctime)s", "module": "%(module)s", "level": "%(levelname)s", "message": "%(message)s"}',
    )

    debug_msg = ", ".join([f"'{arg} = {value}'" for arg, value in args.__dict__.items()])
    logging.debug(f"CLI started with args: {debug_msg}")

    result = {}
    try:
        match args.command:
            case "workspace":
                match args.workspace_command:
                    case "create":
                        result = create_workspace_command(args)
                    case "delete":
                        result = delete_workspace_command(args)
                    case _:
                        parser.print_help()
                # workspace_command(args)
                pass
            case "lakehouse":
                match args.lakehouse_command:
                    case "create":
                        raise NotImplementedError("lakehouse create command not implemented")
                        # result = create_lakehouse_command(args)
                    case "delete":
                        raise NotImplementedError("lakehouse delete command not implemented")
                        # result = delete_lakehouse_command(args)
                    case _:
                        parser.print_help()
            case "notebook":
                match args.notebook_command:
                    case "create":
                        raise NotImplementedError("notebook create command not implemented")
                        # result = create_notebook_command(args)
                    case "delete":
                        raise NotImplementedError("notebook delete command not implemented")
                        # result = delete_notebook_command(args)
                    case _:
                        parser.print_help()
            case _:
                parser.print_help()
    except Exception as e:
        logging.error(e)
        sys.stderr.write(str(e))
        sys.exit(1)

    sys.stdout.write(json.dumps(result))

if __name__ == "__main__":
    main()
