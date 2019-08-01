import socket
from typing import Optional
from abc import ABC, abstractmethod
from threading import Thread, Lock
from list import List


class Server(ABC):

    class NewConnectionHandler(Thread):

        def __init__(self, p_port: int, outer: 'Server'):
            super().__init__()
            self.__server_socket = None
            self._active = False
            self.__outer = outer
            try:
                self.__server_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.__server_socket.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__server_socket.bind(("localhost", p_port))
                self.__server_socket.listen(10)
                self.__server_socket.setblocking(False)
                self._active = True
                self.start()
            except Exception as e:
                pass

        def run(self):
            while self._active:
                try:
                    client_socket, _ = self.__server_socket.accept()
                    client_socket.setblocking(False)
                    self.__outer.add_new_client_message_handler(client_socket)
                    self.__outer.process_new_connection(
                        client_socket.getsockname()[0],
                        client_socket.getsockname()[1]
                    )
                except Exception:
                    pass

        def close(self):
            self._active = False
            if self.__server_socket is not None:
                try:
                    self.__server_socket.close()
                except Exception:
                    pass

    class ClientMessageHandler(Thread):

        class ClientSocketWrapper():

            def __init__(self, p_socket: socket.socket):
                self.__client_socket = p_socket
                self.__client_ip = p_socket.getsockname()[0]
                self.__client_port = p_socket.getsockname()[1]

            def receive(self) -> Optional[str]:
                if self.__client_socket is None:
                    return None

                line = b''
                while True:
                    try:
                        part = self.__client_socket.recv(1)
                        if not part:
                            break

                        if part != b'\n':
                            line += part
                        elif part == b'\n':
                            break
                    except BlockingIOError:
                        continue
                    except Exception:
                        return None
                return line.decode('utf-8')

            def send(self, p_message: str):
                self.__client_socket.sendall(
                    p_message.encode("utf-8"))

            def get_client_ip(self) -> str:
                if self.__client_socket is not None:
                    return self.__client_ip

            def get_client_port(self) -> int:
                if self.__client_socket is not None:
                    return self.__client_port

            def close(self):
                if self.__client_socket is not None:
                    try:
                        self.__client_socket.close()
                    except Exception:
                        pass

        def __init__(self, p_client_socket: socket.socket, outer: 'Server'):
            super().__init__()
            self.__socket_wrapper = Server.ClientMessageHandler.ClientSocketWrapper(
                p_client_socket)
            self.__outer = outer
            self._active = False

            if p_client_socket is not None:
                self._active = True
                self.start()

        def run(self):
            message = None

            while self._active:
                message = self.__socket_wrapper.receive()

                if message is not None:
                    self.__outer.process_message(
                        self.__socket_wrapper.get_client_ip(),
                        self.__socket_wrapper.get_client_port(),
                        message
                    )
                else:
                    a_message_handler = self.__outer.find_client_message_handler(
                        self.__socket_wrapper.get_client_ip(),
                        self.__socket_wrapper.get_client_port()
                    )
                    if a_message_handler is not None:
                        a_message_handler.close()
                        self.__outer.remove_client_message_handler(
                            a_message_handler
                        )
                        self.__outer.process_closing_connection(
                            self.__socket_wrapper.get_client_ip(),
                            self.__socket_wrapper.get_client_port()
                        )

        def send(self, p_message: str):
            if self._active:
                self.__socket_wrapper.send(p_message)

        def close(self):
            if self._active:
                self._active = False
                self.__socket_wrapper.close()

        def get_client_ip(self) -> str:
            return self.__socket_wrapper.get_client_ip()

        def get_client_port(self) -> int:
            return self.__socket_wrapper.get_client_port()

    def __init__(self, p_port: int):
        self.__connection_handler = Server.NewConnectionHandler(p_port, self)
        self.__message_handlers = List['Server.ClientMessageHandler']()
        self.__message_handlers_lock = Lock()

    def is_open(self) -> bool:
        return self.__connection_handler._active

    def is_connected_to(self, p_client_ip: str, p_client_port: int) -> bool:
        a_message_handler = self.find_client_message_handler(
            p_client_ip, p_client_port)

        if a_message_handler is not None:
            return a_message_handler._active
        else:
            return False

    def send(self, p_client_ip: str, p_client_port: int, p_message: str):
        a_message_handler = self.find_client_message_handler(
            p_client_ip, p_client_port)

        if a_message_handler is not None:
            a_message_handler.send(p_message)

    def send_to_all(self, p_message: str):
        with self.__message_handlers_lock:
            a_message_handler = None
            self.__message_handlers.to_first()
            while self.__message_handlers.has_access():
                a_message_handler = self.__message_handlers.get_content()
                if a_message_handler is not None:
                    self.process_closing_connection(
                        a_message_handler.get_client_ip(),
                        a_message_handler.get_client_port()
                    )
                    a_message_handler.close()
                self.__message_handlers.remove()

    def close_connection(self, p_client_ip: str, p_client_port: int):
        a_message_handler = self.find_client_message_handler(
            p_client_ip,
            p_client_port
        )
        if a_message_handler is not None:
            self.process_closing_connection(p_client_ip, p_client_port)
            a_message_handler.close()
            self.remove_client_message_handler(a_message_handler)

    def close(self):
        self.__connection_handler.close()

        with self.__message_handlers_lock:
            a_message_handler = None
            self.__message_handlers.to_first()
            while self.__message_handlers.has_access():
                a_message_handler = self.__message_handlers.get_content()
                self.process_closing_connection(
                    a_message_handler.get_client_ip(),
                    a_message_handler.get_client_port()
                )
                a_message_handler.close()
                self.__message_handlers.remove()

    @abstractmethod
    def process_new_connection(self, p_client_ip: str, p_client_port: int):
        pass

    @abstractmethod
    def process_message(self, p_client_ip: str, p_client_port: int, p_message: str):
        pass

    @abstractmethod
    def process_closing_connection(self, p_client_ip: str, p_client_port: int):
        pass

    def add_new_client_message_handler(self, p_client_socket: socket.socket):
        with self.__message_handlers_lock:
            self.__message_handlers.append(
                Server.ClientMessageHandler(p_client_socket, self)
            )

    def remove_client_message_handler(self, p_client_message_handler: 'Server.ClientMessageHandler'):
        with self.__message_handlers_lock:
            self.__message_handlers.to_first()
            while self.__message_handlers.has_access():
                if p_client_message_handler is self.__message_handlers.get_content():
                    self.__message_handlers.remove()
                else:
                    self.__message_handlers.next()

    def find_client_message_handler(self, p_client_ip: str, p_client_port: int) -> Optional['Server.ClientMessageHandler']:
        a_message_handler = None

        self.__message_handlers.to_first()
        while self.__message_handlers.has_access():
            a_message_handler = self.__message_handlers.get_content()
            if a_message_handler.get_client_ip() == p_client_ip and \
                    a_message_handler.get_client_port() == p_client_port:
                return a_message_handler
            self.__message_handlers.next()

        return None
