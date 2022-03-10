import asyncio
import aiohttp


# async def func1():
#     print('You are in func1!')
#     await asyncio.sleep(2)
#     print('func1 done!')
#
#
# async def func2():
#     print('You are in func2!')
#     await asyncio.sleep(5)
#     print('func2 done!')
#
#
# async def func3():
#     print('You are in func3!')
#     await asyncio.sleep(4)
#     print('func3 done!')
#
# ioloop = asyncio.get_event_loop()
#
# tasks = [
#     ioloop.create_task(func1()),
#     ioloop.create_task(func2()),
#     ioloop.create_task(func3())
# ]
#
# ioloop.run_until_complete(asyncio.wait(tasks))


import asyncio
import logging
import sys
import time

import aiohttp

logger = logging.getLogger('aiohttp_test')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

URL = 'https://api.github.com/events'
MAX_CLIENTS = 2


async def fetch_async(session, pid):
    logger.info(f'Fetch async process {pid} started')
    start = time.time()
    async with session.get(URL) as response:
        datetime = response.headers.get('Date')
    logger.info(f'Process {pid}: {datetime}, took: {time.time() - start} seconds')
    return datetime


async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(
            fetch_async(session, pid)) for pid in range(1, MAX_CLIENTS + 1)]
        await asyncio.gather(*tasks)
    logger.info(f'Process took: {time.time() - start} seconds')


if __name__ == '__main__':
    io_loop = asyncio.get_event_loop()
    try:
        logger.info('Script has been started')
        io_loop.run_until_complete(asynchronous())
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info('Script has been finished')
        io_loop.close()