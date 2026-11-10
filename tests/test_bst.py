import os
import random
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bst import BST  # noqa: E402
from storage import load_csv, load_json, save_json, validate  # noqa: E402

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "data", "sample_menu.csv")


@pytest.fixture
def tree():
    t = BST()
    for item_id, name in [(50, "Soup"), (30, "Salad"), (70, "Steak"), (20, "Bread"),
                          (40, "Pasta"), (60, "Fish"), (80, "Cake")]:
        t.insert(item_id, name, float(item_id) / 10)
    return t


def ids(tree):
    return [i.id for i in tree]


def test_inorder_is_sorted(tree):
    assert ids(tree) == [20, 30, 40, 50, 60, 70, 80]
    assert len(tree) == 7


def test_duplicate_id_updates_instead_of_adding(tree):
    assert tree.insert(40, "Penne", 9.5) is False
    assert len(tree) == 7
    assert tree.search(40).name == "Penne"


def test_search_and_contains(tree):
    assert tree.search(60).name == "Fish"
    assert tree.search(65) is None
    assert 70 in tree and 71 not in tree


@pytest.mark.parametrize("victim", [20, 30, 50, 80])  # leaf, two children, root, leaf
def test_remove_keeps_order(tree, victim):
    assert tree.remove(victim) is True
    expected = [i for i in [20, 30, 40, 50, 60, 70, 80] if i != victim]
    assert ids(tree) == expected
    assert len(tree) == 6


def test_remove_missing_returns_false(tree):
    assert tree.remove(999) is False
    assert len(tree) == 7


def test_remove_everything():
    t = BST()
    keys = list(range(1, 101))
    random.Random(1).shuffle(keys)
    for k in keys:
        t.insert(k, f"item{k}", 1.0)
    random.Random(2).shuffle(keys)
    for k in keys:
        assert t.remove(k)
    assert len(t) == 0 and t.root is None


def test_update_price(tree):
    assert tree.update_price(30, 4.25) is True
    assert tree.search(30).price == 4.25
    assert tree.update_price(31, 1.0) is False


def test_range_search(tree):
    assert [i.id for i in tree.range_search(35, 65)] == [40, 50, 60]
    assert tree.range_search(81, 90) == []


def test_find_by_name_is_case_insensitive(tree):
    assert [i.id for i in tree.find_by_name("s")] == [30, 40, 50, 60, 70]
    assert [i.id for i in tree.find_by_name("CAKE")] == [80]


def test_min_max_height(tree):
    assert tree.min_item().id == 20
    assert tree.max_item().id == 80
    assert tree.height() == 3
    assert BST().height() == 0


def test_sorted_inserts_degrade_height():
    t = BST()
    for k in range(1, 11):
        t.insert(k, "x", 1)
    assert t.height() == 10  # worst case: the tree becomes a linked list


@pytest.mark.parametrize("bad", [("abc", "Tea", 1), (0, "Tea", 1), (1, "  ", 1),
                                 (1, "Tea", "free"), (1, "Tea", -2)])
def test_validate_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        validate(*bad)


def test_validate_cleans_input():
    assert validate(" 7 ", "  Tea ", "2.499") == (7, "Tea", 2.5)


def test_load_sample_csv():
    t = BST()
    loaded, errors = load_csv(t, SAMPLE)
    assert loaded == 5 and errors == []
    assert t.search(101).name == "Margherita Pizza"


def test_load_csv_reports_bad_lines(tmp_path):
    p = tmp_path / "menu.csv"
    p.write_text("id,name,price\n1,Tea,2\n2,Coffee,abc\n3,Juice\n4,Water,0\n", encoding="utf-8")
    t = BST()
    loaded, errors = load_csv(t, str(p))
    assert loaded == 2
    assert len(errors) == 2


def test_json_round_trip(tree, tmp_path):
    path = str(tmp_path / "out" / "menu.json")
    assert save_json(tree, path) == 7
    t2 = BST()
    assert load_json(t2, path) == 7
    assert t2.inorder() == tree.inorder()


def test_degenerate_tree_does_not_hit_recursion_limit():
    t = BST()
    n = 5000                       # sorted inserts: a 5000-deep chain
    for k in range(n):
        t.insert(k, "x", 1)
    assert t.height() == n
    assert [i.id for i in t.range_search(4990, 4999)] == list(range(4990, 5000))
    assert t.remove(0) and t.remove(n - 1) and t.remove(2500)
    assert len(t) == n - 3
