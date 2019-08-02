import socket
from typing import Optional, Dict
from abc import ABC, abstractmethod
from threading import Thread
import select
from queue import Queue, Empty


class Server(ABC):

    class ClientHandler():
        def __init__(self, socket, p_ip, p_port):
            self.__socket = socket
            self.__ip = p_ip
            self.__port = p_port
            self.__send_buffer: Queue[bytes] = Queue()

        @property
        def ip(self):
            return self.__ip

        @property
        def port(self):
            return self.__port

        def close(self):
            try:
                self.__socket.close()
            except Exception:
                pass

        def receive(self):
            message = b''
            while True:
                try:
                    message_part = self.__socket.recv(1)
                    if message_part == b'\n' or message_part == b'':
                        return message.decode("utf-8")
                    else:
                        message += message_part
                except Exception as e:
                    return None

        def send(self, p_message: str):
            print(f"Send to {self.ip}:{self.port}: {p_message}")
            self.__send_buffer.put(p_message.encode("utf-8"))

        def send_from_buffer(self):
            try:
                message = self.__send_buffer.get(block=False)
                if message is not None:
                    try:
                        self.__socket.sendall(message + b'\n')
                    except Exception as e:
                        self.__send_buffer.put(message)
            except Empty:
                pass

    def __init__(self, p_port: int):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind(('127.0.0.1', p_port))
        self.__socket.listen()
        self.__active = True
        self.__clients: Dict[socket.socket, 'Server.ClientHandler'] = {}

        self.__t = Thread(target=self.__run)
        self.__t.start()

    def __run(self):
        while self.__active:
            sockets = [self.__socket] + list(self.__clients.keys())
            read_sockets, _, exception_sockets = select.select(
                sockets, [], sockets)

            for notified_socket in read_sockets:
                if notified_socket == self.__socket:

                    client_socket, client_address = self.__socket.accept()

                    self.__clients[client_socket] = Server.ClientHandler(
                        client_socket, client_address[0], client_address[1])
                    self.process_new_connection(
                        client_address[0], client_address[1])
                    print(
                        f"Accepted new connection from {client_address[0]}:{client_address[1]}")

                else:
                    client = self.__clients[notified_socket]

                    client.send_from_buffer()

                    message = client.receive()
                    if not message:
                        del self.__clients[notified_socket]
                        client.close()
                        continue

                    self.process_message(
                        client_address[0], client_address[1], message)
                    print(
                        f"Received message from {client_address[0]}: {message}")

            for notified_socket in exception_sockets:
                del self.__clients[notified_socket]

    def close(self):
        print("Closing server")
        self.__active = False

        for client_handler in self.__clients.values():
            self.process_closing_connection(
                client_handler.ip, client_handler.port)
            client_handler.close()

        try:
            self.__socket.close()
        except Exception:
            pass

    def is_open(self):
        return self.__active

    def is_connected_to(self, p_client_ip, p_client_port):
        return self.__find_client_handler(p_client_ip, p_client_port) is not None

    def send(self, p_client_ip, p_client_port, p_message):
        client_handler = self.__find_client_handler(p_client_ip, p_client_port)
        client_handler.send(p_message)

    def send_to_all(self, p_message):
        for client_handler in self.__clients.values():
            client_handler.send(p_message)

    def close_connection(self, p_client_ip, p_client_port):
        client_handler = self.__find_client_handler(p_client_ip, p_client_port)
        client_handler.close()

    @abstractmethod
    def process_message(self, p_client_ip, p_client_port, process_message):
        pass

    @abstractmethod
    def process_new_connection(self, p_client_ip, p_client_port):
        pass

    @abstractmethod
    def process_closing_connection(self, p_client_ip, p_client_port):
        pass

    def __find_client_handler(self, p_client_ip, p_client_port):
        for client_handler in self.__clients.values():
            if client_handler.ip == p_client_ip and client_handler.port == p_client_port:
                return client_handler
        return None
