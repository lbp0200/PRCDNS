import argparse
import asyncio
import functools
import json

from dnslib import *

from PRCDNS.proxy_client import ProxyClient


class DNSServerProtocol(asyncio.Protocol):
    args = None
    gFuncs = globals()
    peername = None
    loop = None
    request = None

    def __init__(self, args, loop):
        self.args = args
        self.loop = loop

    def get_data(self, data):
        l = len(data)
        if l == 2:
            return
        sz = struct.unpack(">H", data[:2])[0]
        if sz < l - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > l - 2:
            return data
            # raise Exception("Too big TCP packet")
        return data[2:]

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        if self.args.debug:
            print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        data = self.get_data(data)
        if data is None:
            self.transport.close()
            return
        self.request = DNSRecord.parse(data)
        if self.args.debug:
            print('Data received: {!r}'.format(self.request))

        from IPy import IP
        ip = IP(self.peername[0])
        client_ip = self.peername[0]
        if ip.iptype() == 'PRIVATE':
            client_ip = self.args.myip

        url = 'https://dns.google.com/resolve?name={}&edns_client_subnet={}/24'.format(str(self.request.q.qname),
                                                                                       client_ip)
        # client = ProxyClient()
        # google_dns_resp = client.query_domain(url, self.args.proxy)

        asyncio.ensure_future(ProxyClient.query_domain(url, self.args.proxy), loop=self.loop).add_done_callback(
            functools.partial(self.send_resp))

    def send_resp(self, fut):
        google_dns_resp = fut.result()
        # google_dns_resp = '{"Status": 0,"TC": false,"RD": true,"RA": true,"AD": false,"CD": false,"Question":[ {"name": "img.alicdn.com.","type": 1}],"Answer":[ {"name": "img.alicdn.com.","type": 5,"TTL": 21557,"data": "img.alicdn.com.danuoyi.alicdn.com."},{"name": "img.alicdn.com.danuoyi.alicdn.com.","type": 1,"TTL": 59,"data": "111.32.130.109"},{"name": "img.alicdn.com.danuoyi.alicdn.com.","type": 1,"TTL": 59,"data": "111.32.130.108"}],"Additional":[],"edns_client_subnet": "223.72.90.0/24","Comment": "Response from danuoyinewns1.gds.alicdn.com.(121.43.18.33)"}'
        if self.args.debug:
            print('from: {};response: {}'.format(self.peername[0], google_dns_resp))
        resp = json.loads(google_dns_resp)
        a = self.request.reply()
        if resp['Status'] == 0 and 'Answer' in resp:
            for answer in resp['Answer']:
                qTypeFunc = QTYPE[answer['type']]
                a.add_answer(RR(answer['name'], answer['type'], rdata=self.gFuncs[qTypeFunc](answer['data']),
                                ttl=answer['TTL']))
        elif resp['Status'] == 3 and 'Authority' in resp:
            for answer in resp['Authority']:
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
    coro = loop.create_server(lambda: DNSServerProtocol(args, loop), args.listen, args.port)
    server = loop.run_until_complete(coro)

    try:
        print("public ip is {}".format(myip))
        print("listen on {0}:{1}".format(args.listen, args.port))
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Close Server')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()
