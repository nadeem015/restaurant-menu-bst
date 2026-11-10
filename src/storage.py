"""Load and save the menu as JSON or CSV."""

from __future__ import annotations

import csv
import json
import os

from bst import BST


def validate(item_id, name, price) -> tuple[int, str, float]:
    """Return a cleaned (id, name, price) or raise ValueError."""
    try:
        item_id = int(item_id)
    except (TypeError, ValueError):
        raise ValueError(f"ID must be a whole number, got {item_id!r}")
    if item_id <= 0:
        raise ValueError("ID must be a positive number")
    name = str(name).strip()
    if not name:
        raise ValueError("Name cannot be empty")
    try:
        price = round(float(price), 2)
    except (TypeError, ValueError):
        raise ValueError(f"Price must be a number, got {price!r}")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return item_id, name, price


def save_json(tree: BST, path: str) -> int:
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    data = [item.as_dict() for item in tree]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return len(data)


def load_json(tree: BST, path: str) -> int:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    tree.clear()
    for entry in data:
        tree.insert(*validate(entry["id"], entry["name"], entry["price"]))
    return len(tree)


def load_csv(tree: BST, path: str) -> tuple[int, list[str]]:
    """Add items from an 'id,name,price' CSV (header optional).
    Returns (number loaded, list of error messages for skipped lines)."""
    loaded, errors = 0, []
    with open(path, encoding="utf-8", newline="") as f:
        for line_no, row in enumerate(csv.reader(f), start=1):
            if not row or not "".join(row).strip():
                continue
            if line_no == 1 and row[0].strip().lower() == "id":
                continue
            if len(row) != 3:
                errors.append(f"line {line_no}: expected 3 fields, got {len(row)}")
                continue
            try:
                tree.insert(*validate(*row))
                loaded += 1
            except ValueError as exc:
                errors.append(f"line {line_no}: {exc}")
    return loaded, errors
