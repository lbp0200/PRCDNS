import asyncio

import aiohttp
import async_timeout


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def start(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'http://127.0.0.1/')
        print(html)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))


if __name__ == "__main__":
    main()
