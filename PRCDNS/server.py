import argparse
import asyncio
import json

from dnslib import *

from proxy_client import ProxyClient


class DNSServerProtocol(asyncio.Protocol):
    args = None
    gFuncs = globals()
    peername = None

    def __init__(self, args):
        self.args = args

    def get_data(self, data):
        sz = struct.unpack(">H", data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        if self.args.debug:
            print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        data = self.get_data(data)
        request = DNSRecord.parse(data)
        if self.args.debug:
            print('Data received: {!r}'.format(request))

        from IPy import IP
        ip = IP(self.peername[0])
        client_ip = self.peername[0]
        if ip.iptype() == 'PRIVATE':
            client_ip = self.args.myip

        url = 'https://dns.google.com/resolve?name={}&edns_client_subnet={}/24'.format(str(request.q.qname), client_ip)
        google_dns_resp = ProxyClient.get_url(url, self.args.proxy)
        if self.args.debug:
            print('from: {};response: {}'.format(self.peername[0], google_dns_resp))
        resp = json.loads(google_dns_resp)
        a = request.reply()
        for answer in resp['Answer']:
            qTypeFunc = QTYPE[answer['type']]
            a.add_answer(RR(answer['name'], answer['type'], rdata=self.gFuncs[qTypeFunc](answer['data']),
                            ttl=answer['TTL']))
        if self.args.debug:
            print('Send: {!r}'.format(a))
        b_resp = a.pack()
        b_resp = struct.pack(">H", b_resp.__len__()) + b_resp
        self.transport.write(b_resp)
        self.transport.close()


def get_arg():
    """解析参数"""
    parser = argparse.ArgumentParser(prog='prcdns', description='google dns proxy.')
    parser.add_argument('--debug', help='debug model,default NO', default=False)
    parser.add_argument('-l', '--listen', help='listening IP,default 0.0.0.0', default='0.0.0.0')
    parser.add_argument('-p', '--port', help='listening Port,default 3535', default=3535)
    parser.add_argument('-r', '--proxy', help='Used For Query Google DNS,default direct', default=None)

    return parser.parse_args()


def main():
    args = get_arg()
    myip = ProxyClient.get_url('http://ipinfo.io/json')
    myip = json.loads(myip)
    myip = myip['ip']
    args.myip = myip

    loop = asyncio.get_event_loop()
    loop.set_debug(args.debug)
    # Each client connection will create a new protocol instance
    coro = loop.create_server(lambda: DNSServerProtocol(args), args.listen, args.port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Close Server')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()
