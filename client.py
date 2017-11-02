import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

    def put(self, name_server, value_server, timestamp=None):
        timestamp = timestamp or str(int(time.time()))
        with socket.create_connection((self._host, self._port), self._timeout) as sock:
            data = f"put {name_server:0!s} {value_server:.2f} {timestamp:d}\n"
            try:
                sock.sendall(data.encode())
            except socket.error:
                raise ClientError

    def get(self, name_data):
        with socket.create_connection((self._host, self._port), self._timeout) as sock:
            data = f"get {name_data:0!s}\n"
            try:
                sock.sendall(data.encode())
            except socket.error:
                raise ClientError
            dd = sock.recv(1024)
            dd = dd.decode("utf-8")


class ClientError:
        print("Error client")


def _main():
    # проверка работы клиента
    client = Client("127.0.0.1", 8888)
    client.put("test", 0.5, timestamp=546546)
    client.put("test", 2.0, timestamp=2135)
    client.put("test", 0.5, timestamp=65489)
    client.put("load", 3, timestamp=6546131)
    client.put("load", 4, timestamp=4686513)
    print(client.get("*"))


if __name__ == "__main__":
    _main()