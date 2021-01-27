import requests
import os
from bs4 import BeautifulSoup
import datetime
import tldextract as tld
import time
from db import DB_Handler
from pymongo import MongoClient

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

def web_parser(url, res, hDB):
    # save html code as a file
    # name 변수 정규식으로 걸러내기
    try:
        name = url.replace('https://','').replace('http://','').replace('/', '').replace('\\', '').replace('?', '').replace(':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('#','')
    except Exception as e:
        print('web_parser error :{}, url:'.format(e, url))
        return

    path = os.getcwd() + '\\web\\' + name
    with open(path, 'w', encoding='utf8') as f:
        try:
            f.write(url + '\n')
            f.write(res.text)
        except Exception as e:
            print("FILE CREATE ERROR -> ", e)

            return
    print("Web Parse Success -> ", url)
    return

def get_url(res, hDB):
    # extract new domain in a website
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        lnk = a['href']
        if lnk[-1] != '/':
            lnk = lnk + '/'

        if int('.onion' in lnk) & int('http' in lnk):
            if hDB.is_exist_domain(lnk):
                if hDB.is_exist_url(lnk):
                    continue
                else:
                    #print("insert domain_info : {}".format(lnk))
                    hDB.insert_domain_info(lnk)
            else:
                #print("insert domains/domain_info :{}".format(lnk))
                hDB.insert_domains(lnk)
                hDB.insert_domain_info(lnk)
    return

def run():
    hDB = DB_Handler()

    WholeCnt = 0
    while(1):
        log = 'URL 수집 시작 {}회\t {} \n'.format(WholeCnt, datetime.datetime.now())
        print(log)
        hDB.insert_log(WholeCnt+1)

        urllist = []
        for url in hDB.DB['domain_info'].find({"label": 0}, {"_id": 0, "url": 1}):
            raw = list(url.values())[0]
            urllist.append(raw)

        for url in urllist:
            #print("len of domain : {}".format(len(tld.extract(url).domain)))
            url = url.replace("http//", "")

            #한번 더 테스트
            if (len(tld.extract(url).domain) != 16) and (len(tld.extract(url).domain) != 56):
                hDB.insert_bad_url(url, "DomainError", 1)
                print("domain error", len(tld.extract(url).domain) , tld.extract(url).domain)

            #url get 요청 보내기
            try:
                res = requests.get(url, proxies=proxies, timeout=8)
            except Exception as e:
                print("Request Timeout   -> ", url)
                hDB.insert_bad_url(url, "Timeout", 2)
                continue

            #정상 응답일 경우 해당 url의 html code 및 추가 url 파싱
            if res.status_code == 200:
                web_parser(url, res, hDB)
                get_url(res, hDB)
                hDB.label_update(url)
            else:
            #200이 아닐 경우 bat_status.txt에 url과 응답 번호 저장
                print("status code is not 200: {} -> {}".format(url, res.status_code))
                hDB.insert_bad_url(url, "status_code", res.status_code)

        print("URL 수집 완료\t", datetime.datetime.now())
        WholeCnt += 1

    return

if __name__=="__main__":
    hDB = DB_Handler()
    url = "http://dirnxxdraygbifgc.onion/"
    hDB.insert_domain_info(url)
    hDB.insert_domains(url)
    run()