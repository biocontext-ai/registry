import argparse
import asyncio
import json
import os

import yaml
from rich.console import Console

from .get_mcp_tools import get_tools


def get_accessible_servers() -> set[str]:
    """Check which remote URLs are accessible and return set of accessible server identifiers."""
    remote_mcp_servers = {"mcpServers": {}}

    for server in os.listdir("servers"):
        server_path = os.path.join("servers", server)
        meta_path = os.path.join(server_path, "meta.yaml")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path) as f:
            meta = yaml.safe_load(f)
        server_name = meta.get("identifier")
        url = meta.get("url")
        if url is not None:
            remote_mcp_servers["mcpServers"][server_name] = {"url": url}

    # If no remote servers found, return empty set
    if not remote_mcp_servers["mcpServers"]:
        return set()

    _, failures = asyncio.run(get_tools(remote_mcp_servers, verbose=False, failures_as_tuples=True))

    # Get all server names that were checked
    all_servers = set(remote_mcp_servers["mcpServers"].keys())
    # Accessible servers are those that didn't fail
    failed_server_names = {failure[0] for failure in failures}
    accessible_servers = all_servers - failed_server_names

    return accessible_servers


def main():
    parser = argparse.ArgumentParser(description="Filter out inaccessible remote URLs from registry.json")
    parser.add_argument(
        "--registry-json",
        dest="registry_json_path",
        help="Path to registry.json file (required)",
        required=True,
    )
    args = parser.parse_args()

    console = Console()

    # Get list of accessible servers
    console.print("[cyan]Checking which remote URLs are accessible...[/cyan]")
    accessible_servers = get_accessible_servers()

    if accessible_servers:
        console.print(f"[green]✓[/green] Found {len(accessible_servers)} accessible remote server(s)")
        for server in sorted(accessible_servers):
            console.print(f"    [green]✓[/green] {server}")
    else:
        console.print("[yellow]⚠[/yellow] No accessible remote servers found")

    # Load registry.json
    with open(args.registry_json_path) as f:
        registry_data = json.load(f)

    # Filter out url field for inaccessible servers
    removed_count = 0
    for server_entry in registry_data:
        identifier = server_entry.get("identifier")
        if identifier and identifier not in accessible_servers and "url" in server_entry:
            console.print(f"[yellow]⚠[/yellow] Removing url field from {identifier} (server not accessible)")
            del server_entry["url"]
            removed_count += 1

    # Save modified registry.json
    with open(args.registry_json_path, "w") as f:
        json.dump(registry_data, f, indent=2, ensure_ascii=False)

    if removed_count > 0:
        console.print(f"[yellow]⚠[/yellow] Removed url field from {removed_count} server(s)")
    else:
        console.print("[green]✓[/green] All remote URLs in registry.json are accessible")


if __name__ == "__main__":
    main()
