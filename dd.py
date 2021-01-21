import requests
import socks
import socket
import os
from bs4 import BeautifulSoup
import datetime
import socket
#import getmac
import tldextract as tld
#from urllib.request import urlopen
import time

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

class crawler:

    def isurl_exist(url):
        extract = tld.extract(url)
        domain = "http://{}.{}".format(extract.domain, extract.suffix)

        try:
            res = requests.get(domain, proxies=proxies, timeout=15)
        except:
            print("EXCEPT PASS : ", domain)
            pass

        return res

    def web_parser(url, res):
        # 수정하기 : 파일 이름 도메인 + 서픽스로 하지 말고 http://만 빼고 다 작성하기 -> 모든 페이지 대상
        # save html code as a file
        name = url.replace('https://','').replace('http://','').replace('/', '')
        #path = "{}.{}".format(extract.domain, extract.suffix)
        path = os.getcwd() + '\\web\\' + name
        f = open(path, 'a+', encoding='utf8')
        f.write(res.text)
        f.close()
        print("FILE CREATE: SUCCESS", path)
        return

    def get_url(url, res):
        # extract new domain in a website
        disasm_url = tld.extract(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        with open('new.txt', 'a+') as f:
            for a in soup.find_all('a', href=True):
                if int('.onion' in a['href'])  & int('http' in a['href']): #& int(disasm_url.domain not in a['href'])
                    f.write(a['href'] + "\n")
            f.close()

        return

    #def find_url(path):


if __name__=="__main__":
    #url = ['http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page', 'http://thehiddenwiki.org/']
    with open('url.txt', 'r+') as f:
        urls = f.readlines()

    for i in range(len(urls)):
        url = urls[i].replace('\n','')

        try:
            res = requests.get(url, proxies=proxies, timeout=10)
        except:
            print("EXCEPT PASS \t", url)
            with open("pass.txt", 'a+') as p:
                p.write(url + '\n')
            continue

        if res.status_code == 200:
            crawler.web_parser(url, res)
            crawler.get_url(url, res)
        else:
            print(url,"'s response: ", res.status_code)

'''
    url = 'http://thehiddenwiki.org/'

    res = requests.get(url, proxies=proxies, timeout=10)
    crawler.get_url(url,res)
'''
'''
    for i in range(len(url)):
        res = crawler.isurl_exist(url[i])

        if res.status_code == 200:
            crawler.web_parser(url[i], res)
            crawler.get_url(url[i], res)

'''


'''
    for a in soup.find_all('a', href=True):
        url = a['href']
        if int('.onion' in url) & int(disasm_url.domain not in url) & int('http' in url) :
            
'''