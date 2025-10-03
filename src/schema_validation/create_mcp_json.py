import json
import os

from jsonschema import ValidationError, validate
from rich.console import Console


def main() -> None:
    console = Console()
    server_dir = "servers"
    mcp_json_contents = []
    for folder in os.listdir(server_dir):
        mcp_json_path = os.path.join(server_dir, folder, "mcp.json")
        if os.path.exists(mcp_json_path):
            with open(mcp_json_path) as f:
                mcp_json_content = json.load(f)
            mcp_json_contents.append(mcp_json_content)

    # merge into one mcp.json file
    mcp_json_merged = {"mcpServers": {}}
    for mcp_json_content in mcp_json_contents:
        for key, value in mcp_json_content["mcpServers"].items():
            if key not in mcp_json_merged["mcpServers"]:
                mcp_json_merged["mcpServers"][key] = value

    with open("mcp.json", "w") as f:
        json.dump(mcp_json_merged, f, indent=2, ensure_ascii=False)

    # validate the mcp.json file
    with open("mcp_schema.json") as f:
        mcp_schema = json.load(f)
    with open("mcp.json") as f:
        mcp_json_merged = json.load(f)

    try:
        validate(mcp_json_merged, mcp_schema)
        console.print("[green]✓[/green] merged mcp.json is valid")
    except ValidationError as e:
        console.print(f"[red]✗[/red] merged mcp.json is not valid: {e}")


if __name__ == "__main__":
    main()
