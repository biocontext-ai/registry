import asyncio
import os
import sys

import yaml
from rich.console import Console

from .get_mcp_tools import get_tools


def main():
    console = Console()

    remote_mcp_servers = {"mcpServers": {}}

    for server in os.listdir("servers"):
        server_path = os.path.join("servers", server)
        with open(os.path.join(server_path, "meta.yaml")) as f:
            meta = yaml.safe_load(f)
        server_name = meta.get("identifier")
        url = meta.get("url")
        if url is not None:
            remote_mcp_servers["mcpServers"][server_name] = {"url": url}
    _, failures = asyncio.run(get_tools(remote_mcp_servers, verbose=True))
    if failures:
        console.print("[red]✗[/red] Failed to get tools for the following remote servers:")
        for failure in failures:
            console.print(f"    [red]{failure}[/red]")
        sys.exit(1)
    else:
        console.print("[green]✓[/green] Tools for all remote servers were successfully retrieved")


if __name__ == "__main__":
    main()
