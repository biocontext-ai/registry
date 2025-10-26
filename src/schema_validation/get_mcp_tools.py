import argparse
import asyncio
import json
import sys

from fastmcp import Client
from rich.console import Console


def load_config(mcp_json_path: str) -> dict:
    with open(mcp_json_path) as f:
        config = json.load(f)
    return config


async def get_tools(cfg: dict, *, verbose: bool = False) -> tuple[dict, list[str]]:
    if verbose:
        console = Console()
    grouped: dict[str, dict] = {}
    failures = []
    for server in cfg["mcpServers"]:
        server_cfg = {"mcpServers": {server: cfg["mcpServers"][server]}}
        try:
            client = Client(server_cfg)
            async with client:
                tools = await client.list_tools()

                for tool in tools:
                    name = getattr(tool, "name", None) or (tool.get("name") if isinstance(tool, dict) else str(tool))
                    description = getattr(tool, "description", None) or (
                        tool.get("description", "") if isinstance(tool, dict) else ""
                    )
                    input_schema = (
                        getattr(tool, "inputSchema", None) if not isinstance(tool, dict) else tool.get("inputSchema")
                    )
                    output_schema = (
                        getattr(tool, "outputSchema", None) if not isinstance(tool, dict) else tool.get("outputSchema")
                    )

                    group_key = server
                    if group_key not in grouped:
                        grouped[group_key] = {"tools": []}
                    grouped[group_key]["tools"].append(
                        {
                            "name": name,
                            "description": description,
                            "input_schema": input_schema,
                            "output_schema": output_schema,
                        }
                    )
            if verbose:
                console.print(f"[green]✓[/green] Tools for {server} were successfully retrieved")
        except Exception as e:
            failures.append(f"{server}: {e}")

    output = {"mcp_servers": grouped}
    return output, failures


def main():
    parser = argparse.ArgumentParser(description="List MCP tools and schemas from an mcp.json config")
    parser.add_argument(
        "--config",
        dest="config_path",
        help="Path to mcp.json (required)",
        required=True,
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        help="Path to output file (defaults to stdout if omitted)",
        default=None,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging during tool retrieval",
    )
    args = parser.parse_args()
    cfg = load_config(args.config_path)

    output, failures = asyncio.run(get_tools(cfg, verbose=args.verbose))

    console = Console()

    if args.output_path:
        with open(args.output_path, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    else:
        console.print(json.dumps(output, indent=2))
    if failures:
        console.print("[red]✗[/red] Failed to get tools for the following servers:")
        for failure in failures:
            console.print(f"    [red]{failure}[/red]")
        sys.exit(1)
    else:
        console.print("[green]✓[/green] Tools for all servers were successfully retrieved")


if __name__ == "__main__":
    main()
