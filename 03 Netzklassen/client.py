import socket
import errno
from queue import Queue, Empty
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

    def __init__(self, p_ip: str, p_port: int):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((p_ip, p_port))
        self.__socket.setblocking(False)
        self.__send_buffer: Queue[bytes] = Queue()
        self.__receive_buffer: Queue[bytes] = Queue()
        self.__message_buffer = b''
        self.__active = True

        t = Thread(target=self.__run)
        t.start()

    def __receive_to_buffer(self):
        try:
            message_part = self.__socket.recv(1)
            if message_part == b'\n':
                self.__receive_buffer.put(self.__message_buffer)
                self.__message_buffer = b''
            else:
                self.__message_buffer += message_part
        except Exception:
            pass

    def __send_from_buffer(self):
        try:
            message = self.__send_buffer.get(block=False)
            if message is not None:
                try:
                    print(f"Send {message}")
                    self.__socket.sendall(message)
                except Exception:
                    self.__send_buffer.put(message)
        except Empty:
            pass

    def __run(self):
        while self.__active:
            try:
                # sending
                self.__send_from_buffer()

                # receiving
                self.__receive_to_buffer()

                try:
                    message = self.__receive_buffer.get(block=False)
                    if not message:
                        self.close()
                        print("connection closed by the server")

                    print(f"Received {message}")
                    self.process_message(message.decode("utf-8"))
                except Empty:
                    pass
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    self.__active = False
                    print('Error {e}')

    def close(self):
        try:
            self.__active = False
            self.__socket.close()
        except Exception:
            self.__active = False

    def is_connected(self) -> bool:
        return self.__active

    def send(self, p_message: str):
        self.__send_buffer.put(p_message.encode("utf-8"))

    @abstractmethod
    def process_message(self, p_message: str):
        pass
