#!/usr/bin/env python3

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


def load_starfield_items() -> list[dict[str, Any]]:
    """Load Starfield items from the CSV file and format for Alfred."""
    items = []

    try:
        script_dir = Path(__file__).parent
        csv_path = script_dir / "starfield_items.csv"

        with Path(csv_path).open(encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            items.extend(
                {
                    "uid": row["ID"],
                    "title": row["Name"],
                    "subtitle": f"Item ID: {row['ID'].lstrip('0').upper()}",
                    "arg": f"player.additem {row['ID'].lstrip('0').upper()}",
                    "autocomplete": row["Name"],
                }
                for row in reader
            )

    except FileNotFoundError:
        return [{"title": "Error", "subtitle": "CSV file not found", "valid": False}]
    except Exception as e:
        return [{"title": "Error", "subtitle": f"Failed to process items: {e!s}", "valid": False}]

    return items


def main() -> None:
    """Main function to return the Starfield items in Alfred's JSON format."""
    json_output = json.dumps({"items": load_starfield_items()}, indent=2)
    sys.stdout.write(json_output)


if __name__ == "__main__":
    main()
