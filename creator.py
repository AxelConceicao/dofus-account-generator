import sys
import time
import json
from lxml import html
import requests
from requests.exceptions import Timeout
import urllib.request
import socket
import urllib.error

def is_bad_proxy(pip):    
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://www.example.com')  # change the URL to test here
        sock=urllib.request.urlopen(req, timeout=5)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False

class Creator:
    file = None

    def __init__(self, file):
        self.file = file

    def checkProxy(self, ip, port):
        url = 'https://api.github.com/'
        proxies = {
            "http": 'http://' + ip + ':' + port,
            "https": 'https://' + ip + ':' + port,
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
        except Timeout:
            print('The request timed out')
            return None
        except requests.exceptions.ConnectionError:
            print("Connection refused")
            return None
        return response.status_code
        
    def getLocalProxyList(self):
        proxies = []
        with open('proxies.txt', 'r') as file:
            proxies = file.readlines()
        for proxy in proxies:
            ip, port = proxy.strip('\n').split(':')
            print(self.checkProxy(ip, port))
    
    def getOnlineProxy(self):
        url = 'http://pubproxy.com/api/proxy?api=cDhCQVlKaGlTWXNlRXpLMmxYOHZDZz09&type=https'
        response = requests.get(url)
        currentProxy = json.loads(response.text)['data'][0]['ipPort']
        print('Trying ' + currentProxy)
        if is_bad_proxy(currentProxy):
            print("Bad Proxy %s" % (currentProxy))
        else:
            print("%s is working" % (currentProxy))


    def run(self):
        while True:
            self.getOnlineProxy()
        # self.getLocalProxyList()

        

if __name__ == "__main__":
    filename = 'accounts.txt'
    if (len(sys.argv) == 2):
        filename = sys.argv[1]
    Creator(filename).run()
    # with open(filename, 'a') as w:
    exit(0)