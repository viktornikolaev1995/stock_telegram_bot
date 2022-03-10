import asyncio
import aiohttp
import requests

async def task_1():
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('https://realpython.com/async-io-python/') as response:
            print(response.text)
            response.close()
            return


async def task_2():
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('https://ru.investing.com/portfolio/?portfolioID=MzdkMjRgYj9kMWpuYzVjYA%3D%3D') as response:
            print(response.text)
            response.close()
            return

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(task_1())
    asyncio.run(task_2())
