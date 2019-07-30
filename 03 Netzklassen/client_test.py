import unittest
from client import Client


class MyClient(Client):
    def process_message(self, p_message):
        print(p_message)


class TestClient(unittest.TestCase):
    def test(self):

        client = MyClient("localhost", 8000)
        client.send("Hi")


if __name__ == '__main__':
    unittest.main()
