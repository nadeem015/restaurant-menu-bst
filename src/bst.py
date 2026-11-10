"""Binary Search Tree keyed by menu item ID.

Every operation that follows a single root-to-leaf path (insert, search,
remove, range search) runs in O(h) time, where h is the tree height:
O(log n) for a balanced tree and O(n) in the worst case (IDs inserted in
sorted order). An in-order traversal visits the items in ascending ID order
in O(n).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass
class MenuItem:
    id: int
    name: str
    price: float

    def as_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "price": self.price}


class Node:
    __slots__ = ("item", "left", "right")

    def __init__(self, item: MenuItem):
        self.item = item
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class BST:
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self._size = 0

    # ----- basic properties -------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def __contains__(self, item_id: int) -> bool:
        return self.search(item_id) is not None

    def __iter__(self) -> Iterator[MenuItem]:
        """Iterate items in ascending ID order (iterative in-order traversal)."""
        stack: list[Node] = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.item
            node = node.right

    def clear(self) -> None:
        self.root = None
        self._size = 0

    def height(self) -> int:
        """Number of nodes on the longest root-to-leaf path (0 for an empty tree).
        Level-order traversal, so very deep (degenerate) trees are fine."""
        level = [self.root] if self.root else []
        h = 0
        while level:
            h += 1
            level = [c for n in level for c in (n.left, n.right) if c]
        return h

    # ----- insert / search --------------------------------------------------
    def insert(self, item_id: int, name: str, price: float) -> bool:
        """Insert an item. If the ID already exists its name and price are
        replaced. Returns True if a new item was added, False if updated."""
        new = MenuItem(item_id, name, price)
        if self.root is None:
            self.root = Node(new)
            self._size += 1
            return True
        cur = self.root
        while True:
            if item_id < cur.item.id:
                if cur.left is None:
                    cur.left = Node(new)
                    self._size += 1
                    return True
                cur = cur.left
            elif item_id > cur.item.id:
                if cur.right is None:
                    cur.right = Node(new)
                    self._size += 1
                    return True
                cur = cur.right
            else:
                cur.item.name = name
                cur.item.price = price
                return False

    def search(self, item_id: int) -> Optional[MenuItem]:
        cur = self.root
        while cur:
            if item_id == cur.item.id:
                return cur.item
            cur = cur.left if item_id < cur.item.id else cur.right
        return None

    def update_price(self, item_id: int, price: float) -> bool:
        item = self.search(item_id)
        if item is None:
            return False
        item.price = price
        return True

    # ----- delete -----------------------------------------------------------
    def remove(self, item_id: int) -> bool:
        """Delete the item with this ID. Returns True if it existed."""
        parent, node = None, self.root
        while node and node.item.id != item_id:
            parent, node = node, (node.left if item_id < node.item.id else node.right)
        if node is None:
            return False
        if node.left and node.right:
            # Two children: copy the in-order successor here, then delete the successor.
            succ_parent, succ = node, node.right
            while succ.left:
                succ_parent, succ = succ, succ.left
            node.item = succ.item
            parent, node = succ_parent, succ
        child = node.left or node.right          # at most one child now
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
        return True

    # ----- queries ----------------------------------------------------------
    def inorder(self) -> list[tuple[int, str, float]]:
        return [(i.id, i.name, i.price) for i in self]

    def min_item(self) -> Optional[MenuItem]:
        cur = self.root
        while cur and cur.left:
            cur = cur.left
        return cur.item if cur else None

    def max_item(self) -> Optional[MenuItem]:
        cur = self.root
        while cur and cur.right:
            cur = cur.right
        return cur.item if cur else None

    def range_search(self, low: int, high: int) -> list[MenuItem]:
        """Items with low <= id <= high, in ID order. Skips subtrees that
        cannot contain matching IDs, so it visits far fewer than n nodes."""
        out: list[MenuItem] = []
        stack: list[Node] = []
        node = self.root
        while stack or node:
            while node:                       # go left only while smaller IDs can match
                stack.append(node)
                node = node.left if low < node.item.id else None
            node = stack.pop()
            if low <= node.item.id <= high:
                out.append(node.item)
            node = node.right if node.item.id < high else None
        return out

    def find_by_name(self, text: str) -> list[MenuItem]:
        """Case-insensitive substring search over names (O(n): names are not the key)."""
        needle = text.strip().lower()
        return [i for i in self if needle in i.name.lower()]
