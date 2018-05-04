# PRCDNS
这是一个Google DNS代理   
不同之处在于CDN友好，根据你的IP返回最优的解析结果

基于Python2.7另外开发了一个[prc-dns](https://github.com/lbp0200/prc-dns)，新增IPV6、脱离必须使用代理的限制，支持UDP和TCP。

### 原理
[DNS-over-HTTPS API](https://developers.google.com/speed/public-dns/docs/dns-over-https)   
它支持edns_client_subnet，把你的IP作为参数提交，它会返回最优的解析结果，所以说它
是我见过的最完美的DNS解决方案。

### 测试
```bash
#本人北京联通，对比OPENDNS进行测试，证明PRCDNS是CDN友好的
#23.106.151.177:3535 是我搭建的测试地址，遇到攻击可能会关闭
#seaof-153-125-234-242.jp-tokyo-12.arukascloud.io:31910 部署在日本樱花docker
#208.67.222.222:443  OPENDNS
dig @23.106.151.177 +tcp -p 3535 google.com.hk
dig @208.67.222.222 +tcp -p 443 google.com.hk

dig @23.106.151.177 +tcp -p 3535 img.alicdn.com #123.125.18.108北京联通
dig @seaof-153-125-234-242.jp-tokyo-12.arukascloud.io +tcp -p 31910 img.alicdn.com #123.125.18.108北京联通
dig @208.67.222.222 +tcp -p 443 img.alicdn.com  #69.192.12.15香港
```

### 注意事项：PRCDNS前面一定要放pdnsd或者unbound
1. PRCDNS**只支持TCP查询** 
2. PRCDNS**没有缓存**    

很多二级运营商为了节省成本，减少外网之间的带宽结算费用，对DNS查询做了重点照顾，
防止用户使用114、百度、阿里的公共DNS，强制用户将某些流量大的域名指向它的缓存服务器，
于是UDP成了重灾区，目前TCP没事，114已经支持TCP，百度、阿里还不行。PRCDNS前面放
pdnsd、unbound，即解决了缓存问题，又解决了UDP的问题

### 安装
基于Python 3.5   
```bash
sudo pip3 install PRCDNS
```

### 使用

如果你把PRCDNS部署到VPS上，和SS做邻居，这样在家、公司都能用   
```bash
PRCDNS
```
如果把PRCDNS部署到自己本地的机器或者路由器上，请将SS通过polipo转为http类型，以便于PRCDNS可以访问https://developers.google.com   
```bash
PRCDNS -r http://127.0.0.1:8123
```
请使用Supervisor保证PRCDNS一直运行

### 参数
```bash
--debug 调试模式 选填 默认false
-l 监听IP 选填 默认0.0.0.0
-p 监听端口 选填 默认3535
-r http_proxy 如果PRCDNS可以访问https://developers.google.com就不用填写
```
欢迎通过Issue讨论、提问和给予指导    

### 更多文档
[wiki](https://github.com/lbp0200/PRCDNS/wiki)

### docker 方式运行
1. build： `docker build -t prcdns:latest .`
2. run:  `docker run -p 3535:3535 -d --name prcdns prcdns:latest`
