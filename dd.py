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
        
    def web_parser(url, res):


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
    #url = ['http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page', 'http://thehiddenwiki.org/']
    url = 'http://thehiddenwiki.org/'
    disasm_url = tld.extract(url)
    response = requests.get(url, proxies=proxies)

    #extract new domain
    soup = BeautifulSoup(response.text, 'html.parser')
    b=soup.find_all('a', href=True)
    for a in soup.find_all('a', href=True):
        if int('.onion' in a['href']) & int(disasm_url.domain not in a['href']) & int('http' in a['href']) :
            #print(a['href'])
            start = time.time()
            print(a['href'],':',requests.get(a['href'], proxies=proxies))
            print("time :", time.time() - start)


'''    for i in range(len(url)):
        response = requests.get(url[i], proxies=proxies)
        print(url[i], ': ', response)

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        print(type(response.text))

        #save as a file
        extract = tld.extract(url[i])
        path = "{}.{}".format(extract.domain, extract.suffix)
        path = os.getcwd() + '/web/' + path
        #f = open(path, 'a+', encoding='utf8')
        #f.write(response.text)
        #f.close()'''