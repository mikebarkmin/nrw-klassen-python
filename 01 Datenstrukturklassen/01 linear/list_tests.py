import unittest

from list import List


class TestListNode(unittest.TestCase):
    def test_init(self):
        list = List()

        list_node = list.ListNode(3)

        self.assertEqual(list_node._ListNode__content, 3)

    def test_next(self):
        list = List()

        list_node = list.ListNode(1)
        next_list_node = list.ListNode(2)

        self.assertEqual(list_node.get_next_node(), None)

        list_node.set_next_node(next_list_node)

        self.assertEqual(list_node.get_next_node(), next_list_node)
        self.assertEqual(next_list_node.get_next_node(), None)

    def test_content(self):
        list = List()

        list_node = list.ListNode(1)

        self.assertEqual(list_node.get_content(), 1)


class Testlist(unittest.TestCase):

    def test(self):
        list = List()
        self.assertTrue(list.is_empty())
        self.assertFalse(list.has_access())

        list.insert(3)
        self.assertFalse(list.is_empty())
        self.assertFalse(list.has_access())

        list.to_first()
        self.assertTrue(list.has_access())
        self.assertEqual(list.get_content(), 3)

        list.set_content(4)
        self.assertTrue(list.has_access())
        self.assertEqual(list.get_content(), 4)

        list.append(5)
        self.assertTrue(list.has_access())
        self.assertEqual(list.get_content(), 4)

        list.to_last()
        self.assertTrue(list.has_access())
        self.assertEqual(list.get_content(), 5)

        list.next()
        self.assertFalse(list.has_access())
        self.assertEqual(list.get_content(), None)

        list.to_first()
        list.remove()
        self.assertTrue(list.has_access())
        self.assertEqual(list.get_content(), 5)

    def test_concat(self):
        list1 = List()
        list1.append(1)
        list1.append(2)
        list1.append(3)

        list2 = List()
        list2.append(4)
        list2.append(5)
        list2.append(6)

        list1.concat(list2)

        list1.to_first()
        for i in range(1, 6):
            self.assertEqual(list1.get_content(), i)
            list1.next()

        self.assertTrue(list2.is_empty())


if __name__ == '__main__':
    unittest.main()

