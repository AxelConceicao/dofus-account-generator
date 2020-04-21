import json
import requests
import urllib.request
import socket
import urllib.error
from src import misc

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

def getOnlineProxy():
    url = 'http://pubproxy.com/api/proxy'
    response = requests.get(url)
    try:
        currentProxy = json.loads(response.text)['data'][0]['ipPort']
    except:
        print(response.text)
        misc.ePrint('API may be dead ?')
        exit(1)
    if is_bad_proxy(currentProxy):
        print("Bad Proxy %s" % (currentProxy))
        return None
    else:
        print("%s is working" % (currentProxy))
        return currentProxy
    
def getLocalProxy(filename):
    proxy_list = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            proxy_list.append(line.strip('\n'))
    return proxy_list