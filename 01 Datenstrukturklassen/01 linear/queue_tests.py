import unittest

from queue import Queue


class TestQueueNode(unittest.TestCase):
    def test_init(self):
        queue = Queue()

        queue_node = queue.QueueNode(3)

        self.assertEqual(queue_node._QueueNode__content, 3)

    def test_next(self):
        queue = Queue()

        queue_node = queue.QueueNode(1)
        next_queue_node = queue.QueueNode(2)

        self.assertEqual(queue_node.next, None)

        queue_node.next = next_queue_node

        self.assertEqual(queue_node.next, next_queue_node)
        self.assertEqual(next_queue_node.next, None)

    def test_content(self):
        queue = Queue()

        queue_node = queue.QueueNode(1)

        self.assertEqual(queue_node.content, 1)


class TestQueue(unittest.TestCase):

    def test(self):
        queue = Queue()

        self.assertTrue(queue.is_empty())

        queue.enqueue(3)

        self.assertFalse(queue.is_empty())

        self.assertEqual(queue.front(), 3)

        queue.enqueue(4)

        self.assertEqual(queue.front(), 3)

        queue.dequeue()

        self.assertEqual(queue.front(), 4)

        queue.dequeue()

        self.assertEqual(queue.front(), None)

        queue.dequeue()

        self.assertEqual(queue.front(), None)


if __name__ == '__main__':
    unittest.main()

