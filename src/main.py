"""Console app for managing a restaurant menu stored in a Binary Search Tree."""

from __future__ import annotations

import os

from bst import BST
from storage import load_csv, load_json, save_json, validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "menu.json")
SAMPLE_FILE = os.path.join(ROOT, "data", "sample_menu.csv")

MENU = """
==== Restaurant Menu Management (BST) ====
 1. Add / replace item       6. Search by name
 2. Delete item              7. Items in an ID range
 3. Search by ID             8. Load sample menu
 4. Update price             9. Save menu to file
 5. Show full menu          10. Load menu from file
11. Tree statistics          0. Exit
"""


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(ask(prompt))
        except ValueError:
            print("  Please enter a whole number.")


def print_items(items) -> None:
    items = list(items)
    if not items:
        print("  (no items)")
        return
    print(f"  {'ID':>5}  {'Name':<28} {'Price':>8}")
    print("  " + "-" * 44)
    for it in items:
        print(f"  {it.id:>5}  {it.name:<28} {it.price:>8.2f}")


def main() -> None:
    tree = BST()
    while True:
        print(MENU)
        try:
            choice = ask("Enter choice: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        try:
            if choice == "0":
                break
            elif choice == "1":
                item_id, name, price = validate(ask("ID: "), ask("Name: "), ask("Price: "))
                added = tree.insert(item_id, name, price)
                print("  Added." if added else "  Existing item replaced.")
            elif choice == "2":
                print("  Deleted." if tree.remove(ask_int("ID to delete: ")) else "  No item with that ID.")
            elif choice == "3":
                item = tree.search(ask_int("ID to search: "))
                print_items([item] if item else [])
            elif choice == "4":
                item_id = ask_int("ID to update: ")
                if item_id not in tree:
                    print("  No item with that ID.")
                    continue
                _, _, price = validate(item_id, "x", ask("New price: "))
                tree.update_price(item_id, price)
                print("  Price updated.")
            elif choice == "5":
                print_items(tree)
            elif choice == "6":
                print_items(tree.find_by_name(ask("Name contains: ")))
            elif choice == "7":
                low, high = ask_int("From ID: "), ask_int("To ID: ")
                print_items(tree.range_search(min(low, high), max(low, high)))
            elif choice == "8":
                loaded, errors = load_csv(tree, SAMPLE_FILE)
                print(f"  Loaded {loaded} sample items.")
                for e in errors:
                    print("  Skipped", e)
            elif choice == "9":
                print(f"  Saved {save_json(tree, DATA_FILE)} items to {DATA_FILE}.")
            elif choice == "10":
                if not os.path.exists(DATA_FILE):
                    print("  No saved menu yet. Use option 9 first.")
                else:
                    print(f"  Loaded {load_json(tree, DATA_FILE)} items.")
            elif choice == "11":
                lo, hi = tree.min_item(), tree.max_item()
                print(f"  Items: {len(tree)}   Tree height: {tree.height()}")
                if lo:
                    print(f"  Lowest ID: {lo.id} ({lo.name})   Highest ID: {hi.id} ({hi.name})")
            else:
                print("  Invalid choice.")
        except ValueError as exc:
            print("  Error:", exc)
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("Goodbye!")


if __name__ == "__main__":
    main()
