import asyncio
import aiohttp


class ProxyClient:
    """Google DNS Client"""
    proxy = None

    # def __init__(self, proxy=None):
    #     self.proxy = proxy

    @staticmethod
    async def fetch(session, url, proxy=None):
        with aiohttp.Timeout(10):
            # http://127.0.0.1:8123
            async with session.get(url, proxy=proxy) as response:
                return await response.text()

    @staticmethod
    async def query_domain(url, proxy=None):
        async with aiohttp.ClientSession() as session:
            return await ProxyClient.fetch(session, url, proxy)

    @staticmethod
    async def get(loop, url):
        async with aiohttp.ClientSession(loop=loop) as session:
            return await ProxyClient.fetch(session, url)

    @staticmethod
    def get_url(url, proxy=None):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ProxyClient.get(loop, url))
