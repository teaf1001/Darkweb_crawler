import requests
import os
from bs4 import BeautifulSoup
import datetime
import socket
import getmac

#from urllib.request import urlopen

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050',
}


class crawler:
 '''
    def __init__(self):
        self.url = ''
        self.res = requests.get(self.url, proxies=proxies)
'''

    def web_parser(url, res):
        
        #parse html code
        html = res.text
        parse = BeautifulSoup(html, 'html.parser')
        
        if 'https://' in url:
            savename = url.replace('https://','')
        elif 'http://' in url:
            savename = url.replace('https://','')

        #convert html code to a html file
        f=open("./web/"+savename+".html", 'a+') 
        f.write(parse)
        f.close()
        print("Parse Success ! -->", url)

        return 
    
    def isurl_exist(url):
        res = requests.get(url, proxies=proxies)
        print(res)

        return res

    #def get_url(self):

if __name__=="__main__":
    url = 'https://nate.com'
    res = crawler.isurl_exist(url)

    if res.status_code == 200:
        print("hi")
        crawler.web_parser(url, res)
