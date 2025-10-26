import os
import sys

import yaml
from rich.console import Console


def main():
    console = Console()
    failures = 0
    for folder in os.listdir("servers"):
        if os.path.isdir(os.path.join("servers", folder)):
            with open(os.path.join("servers", folder, "meta.yaml")) as f:
                meta = yaml.safe_load(f)
            expected_folder = meta["identifier"].replace("/", "-")
            if expected_folder != folder:
                console.print(f"[red]✗[/red] Folder name {folder} does not match identifier {expected_folder}")
                failures += 1
    if failures > 0:
        sys.exit(1)
    else:
        console.print("[green]✓[/green] All folder names match identifiers")


if __name__ == "__main__":
    main()
