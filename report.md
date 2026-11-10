# Project Report: Restaurant Menu Management Using a Binary Search Tree

**Author:** M. A. Nadeem Ahmed

## Abstract

This project builds a console-based restaurant menu manager in which every menu item (ID, name and price) is stored in a Binary Search Tree (BST) keyed by its ID. The tree supports insertion, deletion, lookup, price updates, sorted display, ID-range queries and name search. The menu can be saved to JSON and imported from CSV. All tree operations are implemented iteratively, and the system is covered by 24 automated tests. An experiment on tree height confirms that randomly ordered IDs keep the tree shallow, about 28 levels for 5,000 items, while sorted IDs degrade it to a 5,000-level chain. This motivates self-balancing trees as future work.

## 1. Introduction

A restaurant menu changes constantly: dishes are added, removed and repriced, and staff need to find items quickly and print the menu in order. A plain list gives O(n) lookups. A hash table gives fast lookups but no ordering. A BST provides both: O(log n) average lookups and an in-order traversal that yields the items already sorted by ID.

**Objectives**

1. Implement a BST from scratch with insert, search, delete and traversal.
2. Build a usable, crash-resistant console interface on top of it.
3. Persist the menu between sessions.
4. Verify correctness with automated tests and measure how insertion order affects performance.

## 2. Background

A BST is a binary tree in which every node's key is greater than all keys in its left subtree and smaller than all keys in its right subtree. Search, insertion and deletion follow a single path from the root, so their cost is proportional to the tree height *h*. A tree built from randomly ordered keys has an expected height of O(log n). Keys inserted in sorted order produce a degenerate tree with h = n. Self-balancing variants, such as AVL trees and red-black trees, rotate nodes to guarantee h = O(log n).

## 3. System design

```
main.py (console menu)
   |
   |-- storage.py   validate(), load_csv(), load_json(), save_json()
   |
   '-- bst.py       BST of MenuItem(id, name, price)
```

- **`MenuItem`** is a dataclass holding `id`, `name` and `price`.
- **`BST`** owns the root node and a size counter. Each `Node` holds one `MenuItem`.
- **`storage`** validates all external input. IDs must be positive integers, names must be non-empty, and prices must be non-negative numbers rounded to 2 decimal places. It also converts between the tree and files.
- **`main`** is a loop that reads a choice, calls the tree or storage functions, and turns any `ValueError` into a friendly message.

**Duplicate IDs:** inserting an existing ID replaces that item's name and price, so an ID always identifies exactly one dish.

## 4. Implementation

| Operation | Approach |
|---|---|
| Insert | Walk left or right from the root until an empty child is found. Update in place if the ID matches. |
| Search | Iterative walk down one path. |
| Delete | Find the node and its parent. A node with two children is replaced by its in-order successor, the smallest node in its right subtree, which is then unlinked. |
| Sorted display | Iterative in-order traversal with an explicit stack, exposed as a Python iterator. |
| Range query | In-order traversal that only descends left when smaller IDs can still match and only right when larger IDs can. |
| Height | Level-order traversal (counting levels). |
| Name search | Linear scan of the traversal, since names are not the key. |

Every operation is iterative. A recursive version would raise `RecursionError` on a degenerate tree deeper than about 1,000 nodes, Python's default recursion limit. A regression test covers this with a 5,000-node chain.

## 5. Testing

`tests/test_bst.py` contains 24 pytest tests, run automatically by GitHub Actions on every push:

- In-order traversal is sorted, and the size is tracked correctly.
- Duplicate IDs update the item instead of adding a new one.
- Deleting a leaf, a node with two children, and the root keeps the order intact. Deleting 100 random keys empties the tree.
- Range and name queries, min and max, and height.
- Validation rejects five kinds of bad input and cleans valid input.
- CSV import loads the sample menu and reports malformed lines.
- A JSON save-and-load round trip preserves the menu exactly.
- A 5,000-deep degenerate tree works without recursion errors.

All 24 tests pass.

## 6. Experiment: effect of insertion order on height

**Setup:** for n = 100, 1,000 and 5,000, the IDs 0 to n−1 were inserted in 20 random orders (seeds 0–19), and the resulting heights were recorded. Sorted insertion was also measured.

| n | Mean height (random order) | Min | Max | log₂ n | Height (sorted order) |
|---|---|---|---|---|---|
| 100 | 13.4 | 10 | 19 | 6.6 | 100 |
| 1,000 | 22.4 | 20 | 26 | 10.0 | 1,000 |
| 5,000 | 28.2 | 25 | 32 | 12.3 | 5,000 |

**Observations:** random insertion keeps the height within a small constant factor of log₂ n, about 2.3×, which is consistent with the known expected height of a random BST. Sorted insertion produces a chain, so every operation becomes linear. The bundled sample menu has sequential IDs 101–105 and already produces a height-5 chain. This shows that real menus, whose IDs are often assigned sequentially, are the worst case for a plain BST.

## 7. Discussion

The BST is a good fit for this problem: menu display is naturally sorted, range queries ("all items 200–299", for example one menu section) come almost for free, and the code stays small. Its main weakness is the dependence on insertion order measured above. Name search is linear because the tree is keyed by ID. A secondary index, such as a dictionary or a second tree keyed by name, would make it fast.

## 8. Conclusion and future work

The project delivers a complete, tested menu manager built on a hand-written BST and demonstrates both its strengths and its worst case. Possible extensions:

1. Replace the plain BST with an **AVL or red-black tree** to guarantee O(log n) height for sequential IDs.
2. Add a **name index** for fast lookups by dish name.
3. Add **categories** (starters, mains, desserts) and **availability** flags.
4. Provide a **web or GUI front end** that uses the same `bst` and `storage` modules.

## References

1. T. H. Cormen, C. E. Leiserson, R. L. Rivest and C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022. Chapter 12 covers binary search trees.
2. B. Reed, "The height of a random binary search tree," *Journal of the ACM*, 50(3), 2003.
3. Python Software Foundation, *The Python Language Reference*: recursion limit (`sys.getrecursionlimit`).

## Appendix: running the project

```bash
python src/main.py         # interactive menu
python -m pytest -q        # run the test suite
```
