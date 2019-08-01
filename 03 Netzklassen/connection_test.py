import unittest
from connection import Connection
from time import sleep
import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.connection = Connection("localhost", 8888)

    def tearDown(self):
        self.connection.close()

    def test(self):

        s = randomString(300)
        s += "\n"
        self.connection.send(s)
        sleep(2)
        r = self.connection.receive()
        self.assertEqual(r + "\n", s)

    def test_umlate(self):
        s = "üäöß\n"
        self.connection.send(s)
        sleep(2)
        r = self.connection.receive()
        self.assertEqual(r + "\n", s)


if __name__ == '__main__':
    unittest.main()
