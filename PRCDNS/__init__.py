import asyncio

from dnslib import *


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = DNSRecord.parse(data)
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % ('a', addr))
        self.transport.sendto(data, addr)


def main():
    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=('127.0.0.1', 9999))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Close Server')
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()
