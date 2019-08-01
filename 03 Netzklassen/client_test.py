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

        self.socket_wrapper = Client.MessageHandler.SocketWrapper(
            "localhost", 8888)

    def tearDown(self):
        self.client.close()
        self.socket_wrapper.close()

    def test_socket_wrapper(self):
        self.socket_wrapper.send("Hi\n")
        sleep(2)
        r = self.socket_wrapper.receive()
        self.assertEqual("Hi", r)

    def test_client(self):
        sleep(1)
        self.assertTrue(self.client.is_connected())
        self.client.send("Hi\n")
        self.assertTrue(self.client.is_connected())
        sleep(1)
        self.assertEqual("Hi", MyClient.messages[0])


if __name__ == '__main__':
    unittest.main()
