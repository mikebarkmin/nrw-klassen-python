import socket
from typing import Optional
from abc import ABC, abstractmethod
from threading import Thread


class Client(ABC):
    """
    Objekte von Unterklassen der abstrakten Klasse Client ermoeglichen
    Netzwerkverbindungen zu einem Server mittels TCP/IP-Protokoll. Nach
    Verbindungsaufbau koennen Zeichenketten (Strings) zum Server gesendet und von
    diesem empfangen werden, wobei der Nachrichtenempfang nebenlaeufig geschieht.
    Zur Vereinfachung finden Nachrichtenversand und -empfang zeilenweise statt,
    d. h., beim Senden einer Zeichenkette wird ein Zeilentrenner ergaenzt und beim
    Empfang wird dieser entfernt. Jede empfangene Nachricht wird einer
    Ereignisbehandlungsmethode uebergeben, die in Unterklassen implementiert werden
    muss. Es findet nur eine rudimentaere Fehlerbehandlung statt, so dass z.B.
    Verbindungsabbrueche nicht zu einem Programmabbruch fuehren. Eine einmal
    unterbrochene oder getrennte Verbindung kann nicht reaktiviert werden.
    """

    class MessageHandler(Thread):

        class SockerWrapper():

            def __init__(self, p_server_ip: str, p_server_port: int):
                self._socket: Optional[socket.socket] = None

                try:
                    self._socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    self._socket.connect((p_server_ip, p_server_port))
                    self._socket.setblocking(False)
                except Exception:
                    pass

            def receive(self) -> Optional[str]:
                if self._socket is None:
                    return None

                line = ""
                while True:
                    part = self._socket.recv(1)
                    if not part:
                        break

                    text = part.decode("utf-8")
                    if text != "\n":
                        line += text
                    elif text == "\n":
                        break
                return line

            def send(self, p_message: str):
                if self._socket is None:
                    return

                try:
                    self._socket.sendall(p_message.encode("utf-8"))
                except Exception:
                    pass

            def close(self):
                if self._socket is not None:
                    try:
                        self._socket.close()
                    except Exception:
                        pass

        def __init__(self, p_server_ip: str, p_server_port: int, outer: 'Client'):
            super().__init__()
            self.__socket_wrapper = Client.MessageHandler.SockerWrapper(
                p_server_ip, p_server_port)
            self.__outer = outer
            self._active = False

            if self.__socket_wrapper._socket is not None:
                self._active = True
                self.start()

        def run(self):
            message = None

            while self._active:
                message = self.__socket_wrapper.receive()
                if message is not None:
                    self.__outer.process_message(message)
                else:
                    self.close()

        def send(self, p_message: str):
            if self._active:
                self.__socket_wrapper.send(p_message)

        def close(self):
            if self._active:
                self._active = False
                self.__socket_wrapper.close()

    def __init__(self, p_server_ip: str, p_server_port: int):
        self.__message_handler = Client.MessageHandler(
            p_server_ip, p_server_port, self)

    def is_connected(self) -> bool:
        return self.__message_handler._active

    def send(self, p_message: str):
        self.__message_handler.send(p_message)

    def close(self):
        self.__message_handler.close()

    @abstractmethod
    def process_message(self, p_message: str):
        pass
