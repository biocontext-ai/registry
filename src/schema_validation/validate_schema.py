import os
import sys

import json5
import yaml
from jsonschema import ValidationError, validate
from rich.console import Console


def yaml_to_json(yaml_file: str) -> dict:
    """Convert a YAML file to a Python dictionary.

    Args:
        yaml_file: Path to the YAML file to convert.

    Returns:
        dict: The parsed YAML content as a Python dictionary.
    """
    with open(yaml_file) as f:
        return yaml.safe_load(f)


def main() -> None:
    """Validate all meta.yaml files against the schema.

    Checks each meta.yaml file in the servers directory against the defined schema.
    Exits with status code 1 if any validation fails.
    """
    console = Console()
    validation_failed = False

    with open("schema.json") as f:
        schema = json5.load(f)

    # Get all server directories
    server_dirs = [d for d in os.listdir("servers") if os.path.isdir(os.path.join("servers", d))]

    # Validate all meta.yaml files
    meta_files = []
    for server_dir in server_dirs:
        meta_path = os.path.join("servers", server_dir, "meta.yaml")
        if os.path.exists(meta_path):
            try:
                meta = yaml_to_json(meta_path)
                meta_files.append(meta)
                validate(meta, schema)
                console.print(f"[green]✓[/green] {meta_path} is valid")
            except ValidationError as e:
                console.print(f"[red]✗[/red] Error validating {meta_path}:")
                console.print(f"    [red]{e.message}[/red]")
                if e.path:
                    console.print(f"    at path: {'/'.join(str(p) for p in e.path)}")
                validation_failed = True
            except Exception as e:
                console.print(f"[red]✗[/red] Unexpected error validating {meta_path}:")
                console.print(f"    [red]{e!s}[/red]")
                validation_failed = True

    # check that identifiers are unique
    identifiers = [meta["identifier"] for meta in meta_files]
    if len(identifiers) != len(set(identifiers)):
        console.print("[red]✗[/red] Identifiers are not unique")
        validation_failed = True
    else:
        console.print("[green]✓[/green] All identifiers are unique")

    # check that license uses spdx.org format
    for lic in [meta["license"] for meta in meta_files]:
        if not lic.startswith("https://spdx.org/licenses") and not lic == "Unknown":
            console.print(f"[red]✗[/red] License {lic} does not use spdx.org format")
            validation_failed = True

    if validation_failed:
        console.print("\n[red]Schema validation failed![/red]")
        sys.exit(1)
    else:
        console.print("\n[green]All schema validations passed![/green]")


if __name__ == "__main__":
    main()
