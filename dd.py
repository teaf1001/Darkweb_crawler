import requests
import os
from bs4 import BeautifulSoup
import datetime
import tldextract as tld
from db import DB_Handler
import time

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}


def web_parser(url, res):
    # save html code as a file
    # name 변수 정규식으로 걸러내기
    try:
        name = url.replace('https://', '').replace('http://', '').replace('/', '').replace('\\', '').replace('?',
                                                                                                             '').replace(
            ':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('#',
                                                                                                                  '')
    except Exception as e:
        print('web_parser error :{}, url:'.format(e, url))
        return

    path = os.getcwd() + '\\web1\\' + name
    try:
        with open(path, 'w', encoding='utf8') as f:
            try:
                f.write(url + '\n')
                f.write(res.text)
            except Exception as e:
                print("FILE CREATE ERROR -> ", e)
                return
    except:
        return
    # print("Web Parse Success -> ", url)
    return


def get_url(res, hDB):
    new_url = 0
    new_domain = 0
    # extract new domain in a website
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        lnk = a['href'].replace(' ','')

        # 중복 검사
        if hDB.is_exist_url(lnk, 'Bad_Url'):
            continue

        # 예기치 못한 에러 점검
        try:
            if len(lnk) == 0:
                continue
            elif lnk[-1] == '#':
                lnk = lnk.replace('#', '')
            else:
                if lnk[-1] != '/':
                    lnk = lnk + '/'
        except Exception as e:
            print("Error in get_url -> Url: ", lnk, e)
            pass
        # 서픽스, 프로토콜 검사
        suffix = tld.extract(lnk).suffix
        if suffix == 'onion' and 'http' in lnk:
            hDB.insert_domain(lnk)

    return


def run():
    hDB = DB_Handler()
    print(hDB.DB, datetime.datetime.now())
    timeout = 10

    while (1):
        # DB에서 파싱 안한 URL 가져오기
        try:
            url = list(hDB.DB['Domain_Info'].find({"Label": 0}, {"_id": 0, "Url": 1})[0].values())[0]
        except:
            print("탐색 종료")
            return

        # 서픽스 검사
        suffix = tld.extract(url).suffix
        if suffix != 'onion' and suffix != 'ly' and suffix != 'ws':
            hDB.insert_bad_url(url, "Suffix Error", 0)
            print("suffix error", url)
            continue

        # 혹시 모를 디버깅
        if (len(tld.extract(url).domain) != 16) and (len(tld.extract(url).domain) != 56):
            hDB.insert_bad_url(url, "Domain Error", 0)
            continue

        # url에 get 요청 보내기
        try:
            hDB.label_update(url)
            res = requests.get(url, proxies=proxies, timeout=timeout)
            print("get to {}".format(url))
        except Exception as e:
            hDB.insert_bad_url(url, "Timeout", 0)
            continue

        if res.status_code == 200:
            # 정상 응답일 경우 해당 url의 html code 및 추가 url 파싱
            web_parser(url, res)
            hDB.res_code_update(url, res.status_code)
            try:
                get_url(res, hDB)
            except Exception as e:
                print("bs4 error :{}".format(e))
                continue
        else:
            # 200이 아닐 경우 bat_status.txt에 url과 응답 번호 저장
            hDB.insert_bad_url(url, "Status_Code", res.status_code)


if __name__ == "__main__":
    hDB = DB_Handler()
    f = open('new_urls.txt', 'r+')

    urls = f.readlines()
    for url in urls:
        hDB.insert_domain(url.replace('\n',''))
    run()