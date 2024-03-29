import socket
from typing import Optional


class Connection():

    def __init__(self, p_server_ip: str, p_server_port: int):
        self.__socket = None

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setblocking(False)
            self.__socket.connect_ex((p_server_ip, p_server_port))
        except Exception:
            pass

    def receive(self) -> Optional[str]:
        if self.__socket is None:
            return None

        line = b''
        while True:
            try:
                part = self.__socket.recv(1)
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
        if self.__socket is None:
            return

        try:
            self.__socket.sendall(p_message.encode("utf-8"))
        except Exception:
            pass

    def close(self):
        if self.__socket is not None:
            try:
                self.__socket.close()
            except Exception:
                pass
