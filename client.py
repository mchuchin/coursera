import asyncio


class Client:

    try:

        async def put(self):
            while True:
                print("Hello World!")
                await asyncio.sleep(1.0)

        async def get(self):
            pass

    except ClientError:
        print("Error client")
