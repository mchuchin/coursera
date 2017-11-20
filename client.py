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
            data = f"put {name_server} {value_server} {timestamp}\n"
            sock.sendall(data.encode())
            if sock.recv(1024) != b"ok\n\n":
                raise ClientError

    def get(self, name_data):
        with socket.create_connection((self._host, self._port), self._timeout) as sock:
            while True:
                sock.sendall(f"get {name_data}\n".encode())  # отправка данных в bytes
                data_server = sock.recv(1024)  # ожидание (получение) ответа
                if not data_server:
                    raise ClientError
                data_server_de = data_server.decode("utf-8")
                data = {}
                if data_server_de == "":
                    return data
                # разбираем ответ для команды get
                for row in data_server_de.split("\n"):
                    if row == "":
                        break
                    elif row == "ok":
                        continue
                    elif row == "error":
                        raise ClientError
                    key, value, timestamp = row.split()
                    if key not in data:
                        data[key] = []
                    data[key].append((int(timestamp), float(value)))
                return data


class ClientError(Exception):
    pass


"""def _main():
    # проверка работы клиента
    client = Client("127.0.0.1", 8888)
    client.put("test", 0.5, timestamp=546546)
    client.put("test", 2.0, timestamp=2135)
    client.put("test", 0.5, timestamp=65489)
    client.put("load", 3, timestamp=6546131)
    client.put("load", 4, timestamp=4686513)
    print(client.get("*"))


if __name__ == "__main__":
    _main()"""