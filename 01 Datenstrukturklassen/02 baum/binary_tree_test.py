import unittest

from binary_tree import BinaryTree


class TestBinaryTree(unittest.TestCase):

    def test_init_none(self):
        bt = BinaryTree()

        self.assertTrue(bt.is_empty())

    def test_init_content(self):

        bt = BinaryTree(1)

        self.assertFalse(bt.is_empty())
        self.assertEqual(bt.get_content(), 1)

    def test_init_r_tree(self):
        r_bt = BinaryTree(2)
        bt = BinaryTree(1, right_tree=r_bt)

        self.assertFalse(bt.is_empty())
        self.assertEqual(bt.get_right_tree(), r_bt)

    def test_init_l_tree(self):
        l_bt = BinaryTree(2)
        bt = BinaryTree(1, left_tree=l_bt)

        self.assertFalse(bt.is_empty())
        self.assertEqual(bt.get_left_tree(), l_bt)


if __name__ == '__main__':
    unittest.main()
