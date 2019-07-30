import unittest
from connection import Connection


class TestConnection(unittest.TestCase):
    def test(self):

        connection = Connection("localhost", 8000)
        connection.send("Hi")
        connection.close()


if __name__ == '__main__':
    unittest.main()
