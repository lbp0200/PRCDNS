# PRCDNS
这是一个Google DNS代理   
不同之处在于CDN友好，根据你的IP返回最优的解析结果
### 原理
[DNS-over-HTTPS API](https://developers.google.com/speed/public-dns/docs/dns-over-https)   
它支持edns_client_subnet，把你的IP作为参数提交，它会返回最优的解析结果，所以说它是我见过的最完美的DNS解决方案。

### 安装
基于Python 3.5
### 使用
1. 如果你把PRCDNS部署到VPS上，和SS做邻居，这样在家、公司都能用。  
```python
PRCDNS
```
2. 把PRCDNS部署到自己本地的机器或者路由器上
请将SS通过polipo转为http类型，以便于PRCDNS可以访问https://developers.google.com
```python
PRCDNS -r http://127.0.0.1:8123
```

欢迎通过Issue讨论、提问和给予指导    