# PRCDNS
Google DNS Proxy   
准确、CDN友好的DNS服务软件
### 原理
[DNS-over-HTTPS API](https://developers.google.com/speed/public-dns/docs/dns-over-https)   
它支持edns_client_subnet，我理解的是根据IP参数，返回最优的解析结果

### 使用
1. 在VPS上  
```python
python PRCDNS/__init__.py -r http://127.0.0.1:8123
```
2. 在自己的机器上
```python
python PRCDNS/__init__.py
```

欢迎通过Issue讨论、提问和给予指导    