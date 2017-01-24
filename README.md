# PRCDNS
这是一个Google DNS代理   
不同之处在于CDN友好，根据你的IP返回最优的解析结果

### 原理
[DNS-over-HTTPS API](https://developers.google.com/speed/public-dns/docs/dns-over-https)   
它支持edns_client_subnet，把你的IP作为参数提交，它会返回最优的解析结果，所以说它
是我见过的最完美的DNS解决方案。

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

1. 如果你把PRCDNS部署到VPS上，和SS做邻居，这样在家、公司都能用
```python
PRCDNS
```
2. 如果把PRCDNS部署到自己本地的机器或者路由器上，请将SS通过polipo转为http类型，以便于PRCDNS可以访问https://developers.google.com
```python
PRCDNS -r http://127.0.0.1:8123
```

### 参数
```bash
--debug 调试模式 选填 默认false
-l 监听IP 选填 默认0.0.0.0
-p 监听端口 选填 默认3535
-r http_proxy 如果PRCDNS可以访问https://developers.google.com就不用填写
```
欢迎通过Issue讨论、提问和给予指导    