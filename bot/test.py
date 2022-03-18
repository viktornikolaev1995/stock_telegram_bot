import json
import aiohttp
import asyncio
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
id = 8923823
first_name = 'Viktor'
username = 'vik'
data = {
    "id": id,
    "first_name": first_name,
    "username": username,
    "stocks": []
}


async def task1():
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'http://127.0.0.1:8000/users/', json=data) as response:
            print(await response.text())
            print(response.headers)

async def task2(offset, limit):
    async with aiohttp.ClientSession() as session:
        params = {
            'offset': offset,
            'limit': limit
        }
        async with session.get('http://127.0.0.1:8000/users/', params=params) as response:
            print(await response.text())
            print(response.headers)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(task1())
        # loop.create_task(task2(offset=0, limit=5)),
        # loop.create_task(task2(offset=0, limit=6)),
        # loop.create_task(task2(offset=0, limit=10)),
        # loop.create_task(task2(offset=0, limit=20))
    ]

    asyncio.gather(*tasks)
    loop.run_forever()
    loop.close()