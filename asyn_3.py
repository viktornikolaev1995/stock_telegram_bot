import time

import aiohttp
import asyncio

import requests

urls = [
    'http://python.org',
    'http://google.com',
    'https://stackoverflow.com/questions/57349578/asyncio-tasks-using-aiohttp-clientsession',
    'https://ru.wikipedia.org/wiki/Google'
]


async def fetch(session, url):
    async with session.get(url) as response:
        print(response.status)


async def main():
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        cwlist = [loop.create_task(fetch(session, url)) for url in urls]
        await asyncio.gather(*cwlist)


def sync():
    for url in urls:
        response = requests.get(url)
        print(response.status_code)


if __name__ == "__main__":
    print('Asynchronous')
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    spent_time = time.time() - start_time
    print(spent_time)
    print('Synchronous')
    start_time = time.time()
    sync()
    spent_time = time.time() - start_time
    print(spent_time)