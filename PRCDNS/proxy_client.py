import aiohttp
import async_timeout


class ProxyClient:
    """Google DNS Client"""

    async def fetch(self, session, url):
        with async_timeout.timeout(10):
            async with session.get(url, proxy="http://127.0.0.1:8123") as response:
                return await response.json()

    async def query_domain(self, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            return await self.fetch(session,
                                    'https://dns.google.com/resolve?name=img.alicdn.com&edns_client_subnet=223.72.90.21/24')
