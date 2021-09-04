import urllib.request

# API Docs: https://nomics.com/docs/

url = "https://api.nomics.com/v1/currencies/ticker?key=3191d498ffe9ecfd785243325e746df6429281ae&ids=BTC&interval=1d,30d&convert=EUR&per-page=100&page=1"
print(urllib.request.urlopen(url).read())