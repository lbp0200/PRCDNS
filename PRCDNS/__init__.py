import asyncio

from dnslib import *


class EchoServerClientProtocol(asyncio.Protocol):
    def get_data(self, data):
        sz = struct.unpack(">H", data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        data = self.get_data(data)
        request = DNSRecord.parse(data)
        print('Data received: {!r}'.format(request))

        # q = DNSRecord(q=DNSQuestion(str(request.q.qname), QTYPE.ANY))
        a = request.reply()
        a.add_answer(RR(str(request.q.qname), QTYPE.A, rdata=A("1.2.3.4"), ttl=60))
        print('Send: {!r}'.format(a))
        b_resp = a.pack()
        b_resp = struct.pack(">H", b_resp.__len__()) + b_resp
        self.transport.write(b_resp)

        print('Close the client socket')
        self.transport.close()


def main():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 5353)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Close Server')
    server.close()
    loop.close()


if __name__ == "__main__":
    main()
