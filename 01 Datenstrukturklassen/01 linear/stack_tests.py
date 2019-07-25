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

        self.assertEqual(stack_node.next, None)

        stack_node.next = next_stack_node

        self.assertEqual(stack_node.next, next_stack_node)
        self.assertEqual(next_stack_node.next, None)

    def test_content(self):
        stack = Stack()

        stack_node = stack.StackNode(1)

        self.assertEqual(stack_node.content, 1)


class TestStack(unittest.TestCase):

    def test_is_empty(self):
        stack = Stack[str]()
        self.assertTrue(stack.is_empty())

        stack.push(3)
        self.assertFalse(stack.is_empty())


if __name__ == '__main__':
    unittest.main()
