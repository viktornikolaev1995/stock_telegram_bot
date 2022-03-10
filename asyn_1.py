import time

import aiohttp
import asyncio

import requests

#
# async def main():
#
#     async with aiohttp.ClientSession() as session:
#
#         pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
#         async with session.get(pokemon_url) as resp:
#             pokemon = await resp.json()
#             print(pokemon['name'])
#             print(pokemon)
#             resp.close()
#
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())



"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
# start_time = time.time()


# async def main():
#
#     async with aiohttp.ClientSession() as session:
#
#         for number in range(1, 151):
#             pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#             async with session.get(pokemon_url) as resp:
#                 pokemon = await resp.json()
#                 print(number, pokemon['name'])
#
#
# print('Asynchronous')
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())
# print("--- %s seconds ---" % (time.time() - start_time))
#
# print('Synchronous')
# def main():
#     for number in range(1, 151):
#         response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{number}')
#         print(number, response.json()['name'])
#
#
# main()
# print("--- %s seconds ---" % (time.time() - start_time))



"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
start_time = time.time()


async def get_pokemon(session, url):
    async with session.get(url) as resp:
        pokemon = await resp.json()
        return pokemon['name']


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            response = session.get(url)
            tasks.append(asyncio.ensure_future(response))

        original_pokemon = await asyncio.gather(*tasks)
        print(original_pokemon)
        for pokemon in original_pokemon:
            print(pokemon)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))