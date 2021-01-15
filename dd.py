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

    def get_url(url):
        #html code parse
        res = requests.get(url)
        html = res.text
        parse = BeautifulSoup(html, 'html.parser')

        #<a> tag parse
        links= parse.find_all("a")

        #select url
        for tag in links:
            href = tag.attrs['href']

            if str(href)[0] != 'h':
                if "#" in href :
                    continue
                elif str(href)[0] == '/' :
                    href = url + str(href)
                else :
                    href = url + '/' + str(href)
            
            if len(href) <= 4 :
                continue
            if href[-1] == '/':
                href = href[0:-1]
            
            #save url in the html code
            print(href)
            f = open("./test/test.txt", "a+")
            f.write(href)
            f.write("\n")
            f.close()

    #def find_url(path):

if __name__=="__main__":
    url = 'https://naver.com'

    #crawler.get_url(url)

    path = './test/test.txt'

    f = open(path)

    urls = f.readlines()

    for i in range(0, len(urls)):
        if urls[i] != '':
            try:
                print(urls[i], ': ', requests.get(urls[i]))
            except:
                pass
    #print(urls[0], ': ', requests.get(urls[0]))






'''
    if res.status_code == 200:
        print("hi")
        crawler.web_parser(url, res)
    '''

''' def __init__(self):
self.url = ''
self.res = requests.get(self.url, proxies=proxies)'''