# Restaurant Menu Management Using a Binary Search Tree

[![Tests](https://github.com/nadeem015/restaurant-menu-bst/actions/workflows/tests.yml/badge.svg)](https://github.com/nadeem015/restaurant-menu-bst/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A console app for managing a restaurant menu. It stores items in a **Binary Search Tree (BST)** keyed by item ID, written from scratch in Python with no third-party libraries.

```
==== Restaurant Menu Management (BST) ====
 1. Add / replace item       6. Search by name
 2. Delete item              7. Items in an ID range
 3. Search by ID             8. Load sample menu
 4. Update price             9. Save menu to file
 5. Show full menu          10. Load menu from file
11. Tree statistics          0. Exit

Enter choice: 5
     ID  Name                            Price
  --------------------------------------------
    101  Margherita Pizza                 7.99
    102  Veg Burger                       4.50
    103  Caesar Salad                     5.25
```

## Features

- **Insert, delete, search and update** menu items by ID.
- **Sorted menu display** using an in-order traversal.
- **Range queries:** list every item between two IDs while skipping subtrees that can't match.
- **Name search:** case-insensitive substring match.
- **Tree statistics:** item count, height, and lowest and highest IDs.
- **Persistence:** save to and load from JSON, and import items from CSV.
- **Input validation:** bad IDs, empty names and negative or non-numeric prices are rejected with a clear message instead of crashing.
- **Iterative algorithms:** no recursion-depth limit, even for a worst-case 5,000-deep tree.
- **Tests:** 24 pytest tests that run automatically on every push (Python 3.11 and 3.13).

## Complexity

| Operation | Average (random IDs) | Worst case (sorted IDs) |
|---|---|---|
| Insert / search / delete / update | O(log n) | O(n) |
| Range query (k results) | O(log n + k) | O(n) |
| Sorted display, name search | O(n) | O(n) |

Inserting IDs in sorted order turns the tree into a chain. The [report](report.md) measures this effect and discusses self-balancing trees as the fix.

## Getting started

Requires Python 3.10 or newer. There are no dependencies.

```bash
python src/main.py
```

Choose **8** to load the sample menu from `data/sample_menu.csv`, then **5** to display it.

### CSV import format

```csv
id,name,price
101,Margherita Pizza,7.99
102,Veg Burger,4.50
```

The header row is optional. Invalid lines are skipped and reported.

## Running the tests

```bash
pip install pytest
python -m pytest -q
```

## Project structure

```
src/
  bst.py        # BST: insert, search, delete, range query, traversal, height
  storage.py    # validation plus JSON and CSV loading and saving
  main.py       # interactive console menu
tests/
  test_bst.py   # unit tests for the tree, validation and file handling
data/
  sample_menu.csv
report.md       # project report: design, analysis and results
```

## License

[MIT](LICENSE)
