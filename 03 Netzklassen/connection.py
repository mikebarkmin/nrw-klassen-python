import socket
from typing import Optional


class Connection():

    def __init__(self, p_server_ip: str, p_server_port: int):
        self.__socket = None

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((p_server_ip, p_server_port))
        except Exception:
            pass

    def receive(self) -> Optional[str]:
        if self.__socket is None:
            return None

        try:
            line = ""
            while True:
                part = self.__socket.recv(1)
                if not part:
                    break

                text = part.decode("utf-8")
                if text != "\n":
                    line += text
                elif text == "\n":
                    break
            return line
        except Exception:
            pass

        return None

    def send(self, p_message: str):
        if self.__socket is None:
            return

        self.__socket.send(p_message.encode("utf-8"))

    def close(self):
        if self.__socket is not None:
            try:
                self.__socket.close()
            except Exception:
                pass
