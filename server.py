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
            response = 'ok\n'
            for key, value in data.items():
                for v in sorted(value):
                    response += f"{key} {value[v]} {v}\n"
            response += '\n'
            return response
        else:
            value = data.get(key)
            if value:
                response = 'ok\n'
                for v in sorted(value):
                    response += f"{key} {value[v]} {v}\n"
                response += '\n'
                return response
            else:
                return 'ok\n\n'


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
