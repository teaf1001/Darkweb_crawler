import requests
import os
from bs4 import BeautifulSoup
import datetime
import tldextract as tld
import time
from db import domain
from pymongo import MongoClient

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

DB_Client = MongoClient("mongodb://localhost:27017/")
DB = DB_Client["DBtest100"]

def web_parser(url, res):
    # 수정하기 : 파일 이름 도메인 + 서픽스로 하지 말고 http://만 빼고 다 작성하기 -> 모든 페이지 대상
    # save html code as a file
    # name 변수 정규식으로 걸러내기
    try:
        name = url.replace('https://','').replace('http://','').replace('/', '').replace('\\', '').replace('?', '').replace(':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('#','')
    except Exception as e:
        print('web_parser error :{}, url:'.format(e, url))
        return

    #extract = tld.extract(url)
    #name = "{}.{}".format(extract.domain, extract.suffix)

    path = os.getcwd() + '\\web\\' + name
    with open(path, 'w', encoding='utf8') as f:
        try:
            f.write(url + '\n')
            f.write(res.text)
        except Exception as e:
            print("FILE CREATE ERROR -> ", e)
    print("Web Parse Success -> ", url)
    return

def get_url(res, cDB):
    # extract new domain in a website
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a', href=True):

        if int('.onion' in a['href']) & int('http' in a['href']):
            if cDB.is_exist_domain(a['href']):
                if cDB.is_exist_url([a['href']]):
                    continue
                else:
                    cDB.insert_domain_info(a['href'])

            else:
                cDB.insert_domains(a['href'])
                cDB.insert_domain_info(a['href'])
    return

#def find_url(path):

def run():
    cDB = domain()

    WholeCnt = 0
    while(1):

        log = 'URL 수집 시작 {}회\t {} \n'.format(WholeCnt, datetime.datetime.now())
        print(log)
        cDB.insert_log(log)

        urllist = []
        for url in DB['domain_info'].find({"label": 0}, {"_id": 0, "url": 1}):
            raw = list(url.values())[0]
            urllist.append(raw)

        for url in urllist:
            #url get 요청 보내기
            try:
                res = requests.get(url, proxies=proxies, timeout=10)
            except Exception as e:
                print("Request Timeout   -> ", url)
                cDB.label_update(url)
                cDB.insert_bad_url(url, "Timeout")
                continue

            #정상 응답일 경우 해당 url의 html code 및 추가 url 파싱
            if res.status_code == 200:
                web_parser(url, res)
                get_url(res, cDB)
                cDB.label_update(url)
                continue

            else:
            #200이 아닐 경우 bat_status.txt에 url과 응답 번호 저장
                print("response status code is not 200: {} -> {}".format(url, res.status_code))
                cDB.insert_status_code(url, res.status_code)
                cDB.label_update(url)
                continue

        print("URL 수집 완료\t", datetime.datetime.now())
        WholeCnt += 1

    return

if __name__=="__main__":
    run()