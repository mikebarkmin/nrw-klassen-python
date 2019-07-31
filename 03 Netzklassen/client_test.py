import unittest
from client import Client
from time import sleep


class MyClient(Client):
    messages = []

    def process_message(self, p_message):
        if p_message is not None:
            MyClient.messages.append(p_message)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = MyClient("localhost", 8888)

    def tearDown(self):
        self.client.close()

    def test(self):
        sleep(1)
        self.assertTrue(self.client.is_connected())
        self.client.send("Hi")
        sleep(1)
        self.assertEqual("Hi", MyClient.messages[0])


if __name__ == '__main__':
    unittest.main()
