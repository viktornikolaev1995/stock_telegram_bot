import aiohttp
import asyncio

MAX_CLIENTS = 3
URL = 'https://api.github.com/events'

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:
            tasks = [asyncio.ensure_future(
                fetch_async(session, pid)) for pid in range(1, MAX_CLIENTS + 1)]
            await asyncio.gather(*tasks)

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")


async def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            print(response.status)
            html = await response.text()
            datetime = session.headers.get('Date')
            print(datetime)
        # response = session.get(URL)#await aiohttp.request('GET', URL)
        # # print(response.)
        # datetime = session.headers.get('Date')#response.headers.get('Date')
        # print(datetime)

            print('Process {}: {}, took: {:.2f} seconds'.format(
                pid, datetime, time.time() - start))

            response.close()
            return

loop = asyncio.get_event_loop()
loop.run_until_complete(main())