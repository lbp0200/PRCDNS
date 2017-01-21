import asyncio
import json
from PRCDNS.proxy_client import ProxyClient
from dnslib import *


class EchoServerClientProtocol(asyncio.Protocol):
    gFuncs = globals()

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

        google_dns_resp = """{"Status": 0,"TC": false,"RD": true,"RA": true,"AD": false,"CD": false,"Question":[ {"name": "img.alicdn.com.","type": 1}],"Answer":[ {"name": "img.alicdn.com.","type": 5,"TTL": 85493,"data": "img.alicdn.com.danuoyi.alicdn.com."},{"name": "img.alicdn.com.danuoyi.alicdn.com.","type": 1,"TTL": 59,"data": "111.32.130.108"},{"name": "img.alicdn.com.danuoyi.alicdn.com.","type": 1,"TTL": 59,"data": "111.32.130.109"}],"Additional":[],"edns_client_subnet": "223.72.90.0/24","Comment": "Response from danuoyinewns3.gds.alicdn.com.(121.42.1.129)"}"""
        resp = json.loads(google_dns_resp)
        a = request.reply()
        for answer in resp['Answer']:
            qTypeFunc = QTYPE[answer['type']]
            a.add_answer(RR(answer['name'], answer['type'], rdata=self.gFuncs[qTypeFunc](answer['data']),
                            ttl=answer['TTL']))
        print('Send: {!r}'.format(a))
        b_resp = a.pack()
        b_resp = struct.pack(">H", b_resp.__len__()) + b_resp
        self.transport.write(b_resp)

        print('Close the client socket')
        self.transport.close()


def main():
    # print(locals()['CNAME']('img.alicdn.com.danuoyi.alicdn.com.'))
    loop = asyncio.get_event_loop()
    client = ProxyClient()
    loop.run_until_complete( client.query_domain(loop))
    print(

    )
    exit()
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
