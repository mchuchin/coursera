import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        '127.0.0.1', 8888
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


def process_data(data):
    status, payload = data.split(" ", 1)
    if status == "get":
        return get(payload)
    elif status == "put":
        return put(payload)
    else:
        return "error\nwrong command\n\n"


def get(key):
    data = dictionary
    keys = key.split("\n")
    for key in keys:
        if key == "":
            continue
        if key == "*":
            responses = {}
            for key, timestamp_data in data.items():
                responses[key] = sorted(timestamp_data.items())
            rows = []
            for response in responses:
                if not response:
                    continue
                for key, values in response.items():
                    for timestamp, value in values:
                        rows.append(f"{key} {value} {timestamp}")

            result = "ok\n"

            if rows:
                result += "\n".join(rows) + "\n"

            return result + "\n"
        else:
            pass


#get <key>\n
#Успешный ответ от сервера:
#ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
#Если ни одна метрика не удовлетворяет условиям поиска, то вернется ответ:
#ok\n\n

def put(data):
    key, value, timestamp = data.split()
    if key not in dictionary:
        dictionary[key] = {}
        dictionary[key][timestamp] = value
    else:
        dictionary[key][timestamp] = value
    return "ok\n\n"

dictionary = {}


run_server()
