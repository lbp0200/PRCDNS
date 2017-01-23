import asyncio

import aiohttp
import async_timeout


class ProxyClient:
    """Google DNS Client"""
    proxy = None

    def __init__(self, proxy=''):
        self.proxy = proxy

    async def fetch(self, session, url):
        with async_timeout.timeout(10):
            # http://127.0.0.1:8123
            async with session.get(url, proxy=self.proxy) as response:
                return await response.text()

    async def query_domain(self, loop):
        async with aiohttp.ClientSession(loop=loop, headers={
            'User-Agent': 'curl/7.21.3 (i686-pc-linux-gnu) libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'}) as session:
            return await self.fetch(session,
                                    'https://dns.google.com/resolve?name=img.alicdn.com&edns_client_subnet=223.72.90.21/24')

    async def get(self, loop, url):
        async with aiohttp.ClientSession(loop=loop) as session:
            return await self.fetch(session, url)

    @staticmethod
    def get_url(url, proxy=None):
        loop1 = asyncio.new_event_loop()
        client = ProxyClient(proxy)
        return loop1.run_until_complete(client.get(loop1, url))
