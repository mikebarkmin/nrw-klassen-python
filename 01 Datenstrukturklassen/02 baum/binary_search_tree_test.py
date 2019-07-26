import unittest

from binary_search_tree import BinarySearchTree
from comparable_content import ComparableContent


class ComparableInt(ComparableContent):

    def __init__(self, i):
        self.i = i

    def is_greater(self, ci):
        return self.i > ci.i

    def is_less(self, ci):
        return self.i < ci.i

    def is_equal(self, ci):
        return self.i == ci.i


class TestBinarySearchTree(unittest.TestCase):

    def test_init(self):
        bt = BinarySearchTree()

        self.assertTrue(bt.is_empty())

    def test(self):
        bt = BinarySearchTree()
        bt.insert(ComparableInt(3))
        self.assertFalse(bt.is_empty())

        bt.insert(ComparableInt(2))
        bt.insert(ComparableInt(4))
        self.assertEqual(bt.get_content().i, 3)
        self.assertEqual(bt.get_left_tree().get_content().i, 2)
        self.assertEqual(bt.get_right_tree().get_content().i, 4)

        bt.remove(ComparableInt(3))
        self.assertEqual(bt.get_content().i, 4)
        self.assertEqual(bt.get_left_tree().get_content().i, 2)
        self.assertEqual(bt.get_right_tree().get_content(), None)

        bt.insert(ComparableInt(2))
        bt.insert(ComparableInt(8))
        bt.insert(ComparableInt(7))
        bt.insert(ComparableInt(2))
        bt.insert(ComparableInt(4))
        bt.insert(ComparableInt(6))
        bt.insert(ComparableInt(3))
        bt.insert(ComparableInt(9))

        self.assertEqual(bt.search(ComparableInt(7)).i, 7)


if __name__ == '__main__':
    unittest.main()
