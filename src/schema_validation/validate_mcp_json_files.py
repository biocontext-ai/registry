import json
import os
import sys

import yaml
from rich.console import Console


def load_yaml_identifier(meta_path: str) -> str:
    with open(meta_path) as f:
        meta = yaml.safe_load(f)
    identifier = meta.get("identifier")
    return identifier


def load_mcp_server_keys(mcp_path: str) -> list[str]:
    with open(mcp_path) as f:
        data = json.load(f)
    return list(data["mcpServers"].keys())


def expected_server_name(identifier: str) -> str:
    # Normalize by replacing '/' with '-' (keeps existing case and hyphens as-is)
    return identifier.replace("/", "-")


def validate_directory(server_dir: str) -> tuple[bool, str]:
    """Validate one server directory.

    Returns (ok, message)
    """
    meta_path = os.path.join(server_dir, "meta.yaml")
    mcp_path = os.path.join(server_dir, "mcp.json")

    if not os.path.exists(mcp_path):
        # No mcp.json → skip (only validate folders that define an MCP server entry)
        return True, "skipped (no mcp.json)"

    if not os.path.exists(meta_path):
        return False, "meta.yaml is missing while mcp.json exists"

    identifier = load_yaml_identifier(meta_path)
    expected = expected_server_name(identifier)
    keys = load_mcp_server_keys(mcp_path)

    if len(keys) != 1:
        return (
            False,
            f"mcp.json must contain exactly 1 server key matching '{expected}', found: {keys!r}",
        )

    found = keys[0]
    if found != expected:
        return (
            False,
            f"mismatch: expected '{expected}' from identifier '{identifier}', found '{found}'",
        )

    return True, "ok"


def validate_mcp_file(mcp_path: str) -> tuple[bool, str]:
    """Validate a specific mcp.json file by resolving its sibling meta.yaml.

    Returns (ok, message)
    """
    if not os.path.exists(mcp_path):
        return False, "mcp.json does not exist"

    server_dir = os.path.dirname(mcp_path)
    meta_path = os.path.join(server_dir, "meta.yaml")

    if not os.path.exists(meta_path):
        return False, "meta.yaml is missing while mcp.json exists"

    identifier = load_yaml_identifier(meta_path)
    expected = expected_server_name(identifier)
    keys = load_mcp_server_keys(mcp_path)

    if len(keys) != 1:
        return (
            False,
            f"mcp.json must contain exactly 1 server key matching '{expected}', found: {keys!r}",
        )

    found = keys[0]
    if found != expected:
        return (
            False,
            f"mismatch: expected '{expected}' from identifier '{identifier}', found '{found}'",
        )

    return True, "ok"


def main() -> None:
    console = Console()
    args = sys.argv[1:]

    results: dict[str, tuple[bool, str]] = {}

    # If file paths were provided (e.g., by pre-commit), validate only mcp.json files.
    if len(args) > 0:
        mcp_paths = [p for p in args if p.endswith("mcp.json")]

        # If no mcp.json files are provided, do nothing and succeed.
        if len(mcp_paths) == 0:
            console.print("No mcp.json paths provided; skipping validation.")
            sys.exit(0)

        for mcp_path in mcp_paths:
            console.print(f"Validating {mcp_path}")
            try:
                ok, message = validate_mcp_file(mcp_path)
            except Exception as e:  # defensive: surface any unexpected error as failure
                ok, message = False, str(e)
            results[mcp_path] = (ok, message)
    else:
        # Legacy behavior: validate all server directories under servers/
        servers_root = os.path.join("servers")
        for name in sorted(os.listdir(servers_root)):
            full_dir = os.path.join(servers_root, name)
            console.print(f"Validating {full_dir}")
            try:
                ok, message = validate_directory(full_dir)
            except Exception as e:  # defensive: surface any unexpected error as failure
                ok, message = False, str(e)
            results[full_dir] = (ok, message)

    failures = {d: msg for d, (ok, msg) in results.items() if not ok}

    if len(failures) > 0:
        # iterate over failures and print the full path
        for d, msg in failures.items():
            console.print(f"[red]✗[/red] {d}: {msg}")
        sys.exit(1)
    else:
        console.print("[green]✓[/green] All validations passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
