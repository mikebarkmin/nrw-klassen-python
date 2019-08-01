import unittest

from time import sleep
from server import Server
from client import Client


class MyServer(Server):

    messages = []

    def process_new_connection(self, p_client_ip, p_client_port):
        self.send(p_client_ip, p_client_port, "Hi\n")

    def process_message(self, p_client_ip, p_client_port, p_message):
        MyServer.messages.append(p_message)

    def process_closing_connection(self, p_client_ip, p_client_port):
        self.send(p_client_ip, p_client_port, "Tschüss\n")


class MyClient(Client):
    messages = []

    def process_message(self, p_message):
        MyClient.messages.append(p_message)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = MyServer(8080)
        sleep(1)
        self.client = MyClient("localhost", 8080)
        sleep(1)

    def tearDown(self):
        self.server.close()
        self.client.close()

    def test(self):
        self.assertTrue(self.server.is_open())
        self.assertTrue(self.client.is_connected())
        self.assertEqual(MyClient.messages[0], "Hi")
        self.assertTrue(self.client.is_connected())

        sleep(2)
        self.server.close()
        sleep(2)
        self.assertEqual(MyClient.messages[1], "Tschüss")
        self.client.close()


if __name__ == '__main__':
    unittest.main()
