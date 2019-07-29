import unittest

from stack import Stack


class TestStackNode(unittest.TestCase):
    def test_init(self):
        stack = Stack()

        stack_node = stack.StackNode(3)

        self.assertEqual(stack_node._StackNode__content, 3)

    def test_next(self):
        stack = Stack()

        stack_node = stack.StackNode(1)
        next_stack_node = stack.StackNode(2)

        self.assertEqual(stack_node.get_next(), None)

        stack_node.set_next(next_stack_node)

        self.assertEqual(stack_node.get_next(), next_stack_node)
        self.assertEqual(next_stack_node.get_next(), None)

    def test_content(self):
        stack = Stack()

        stack_node = stack.StackNode(1)

        self.assertEqual(stack_node.get_content(), 1)


class TestStack(unittest.TestCase):

    def test(self):
        stack = Stack[str]()
        self.assertTrue(stack.is_empty())

        stack.push(3)
        self.assertFalse(stack.is_empty())

        self.assertEqual(stack.top(), 3)

        stack.push(4)

        self.assertEqual(stack.top(), 4)

        stack.pop()

        self.assertEqual(stack.top(), 3)

        stack.pop()

        self.assertEqual(stack.top(), None)

        stack.pop()

        self.assertEqual(stack.top(), None)


if __name__ == '__main__':
    unittest.main()
