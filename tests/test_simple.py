# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import asyncio
import unittest

from dnslib import *


class TestDict(unittest.TestCase):
    def test_init(self):
        self.assertEqual(1, 1)
        # def test_demo(self):

    def test_dig(self):
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(self.tcp_echo_client(loop)),
            asyncio.ensure_future(self.tcp_echo_client(loop)),
            asyncio.ensure_future(self.tcp_echo_client(loop)),
            asyncio.ensure_future(self.tcp_echo_client(loop)),
            asyncio.ensure_future(self.tcp_echo_client(loop)), ]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

    @asyncio.coroutine
    def tcp_echo_client(self, loop):
        reader, writer = yield from asyncio.open_connection('127.0.0.1', 3535,
                                                            loop=loop)

        d = DNSRecord.question("google.com")
        q = d.pack()
        b_req = struct.pack(">H", q.__len__()) + q
        writer.write(b_req)

        data = yield from reader.read()
        resp = DNSRecord.parse(data)
        print('Received: %r' % resp)

        print('Close the socket')
        writer.close()


if __name__ == '__main__':
    unittest.main()
