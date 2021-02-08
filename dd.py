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

def web_parser(url, res, hDB):
    # save html code as a file
    # name 변수 정규식으로 걸러내기
    try:
        name = url.replace('https://','').replace('http://','').replace('/', '').replace('\\', '').replace('?', '').replace(':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('#','')
    except Exception as e:
        print('web_parser error :{}, url:'.format(e, url))
        return

    path = os.getcwd() + '\\web\\' + name
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
    #print("Web Parse Success -> ", url)
    return

def get_url(res, hDB):
    new_url = 0
    new_domain = 0
    # extract new domain in a website
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        lnk = a['href']
        lnk = lnk.replace(' ','')

        #예기치 못한 에러 점검
        try:
            if len(lnk) == 0 :
                continue
            else:
                if lnk[-1] != '/':
                    lnk = lnk + '/'
        except Exception as e:
            print("Error in get_url -> Url: ", lnk, e)
            pass
        #서픽스, 프로토콜 검사
        if (tld.extract(lnk).suffix == 'onion') and ('http' in lnk):
            if hDB.is_exist_url(lnk, 'Domains'):
                if hDB.is_exist_url(lnk, 'Domain_Info'):
                    continue
                else:
                    #print("insert domain_info : {}".format(lnk))
                    hDB.insert_domain_info(lnk)
                    new_url += 1
            else:
                #print("insert domains/domain_info :{}".format(lnk))
                hDB.insert_domains(lnk)
                hDB.insert_domain_info(lnk)
                new_domain += 1
                new_url += 1
    #print("get_url:{},{}".format(new_domain,new_url))
    return new_domain, new_url

def run():
    hDB = DB_Handler()
    print(hDB.DB)
    timeout = 4
    WholeCnt = 1
    while(1):
        log = 'URL 수집 {}회 시작\t\t\t\t\t{}'.format(WholeCnt, datetime.datetime.now())
        print(log)
        hDB.insert_log(WholeCnt, (0,0))

        _new_url = [0, 0]

        urllist = []
        #DB에서 파싱 안한 URL 가져오기
        for url in hDB.DB['Domain_Info'].find({"Label": 0}, {"_id": 0, "Url": 1}):
            raw = list(url.values())[0]
            urllist.append(raw)

        for url in urllist:
            #print("len of domain : {}".format(len(tld.extract(url).domain)))
            url = url.replace("http//", "").replace("#",'')

            #서픽스 검사
            if tld.extract(url).suffix != 'onion':
                hDB.insert_bad_url(url, "Suffix Error", 0)
                hDB.label_update(url)
                continue
            #혹시 모를 디버깅
            if (len(tld.extract(url).domain) != 16) and (len(tld.extract(url).domain) != 56):
                hDB.insert_bad_url(url, "Domain Error", 1)
                hDB.label_update(url)
                print("Domain Error", len(tld.extract(url).domain) , tld.extract(url).domain, url)
                continue
            #중복 검사
            if hDB.is_exist_url(url, 'Bad_Url'):
                continue

            start = time.time()

            #url에 get 요청 보내기
            try:
                res = requests.get(url, proxies=proxies, timeout=5)
            except Exception as e:
                #print("Request Timeout   -> ", url)
                hDB.insert_bad_url(url, "Timeout", timeout)
                hDB.label_update(url)
                continue
            #정상 응답일 경우 해당 url의 html code 및 추가 url 파싱
            if res.status_code == 200:
                end = time.time() - start
                with open('time_{}.txt'.format(hDB.dbname), 'a+')as f:
                    f.write(str(end) + '\n')

                web_parser(url, res, hDB)

                try:
                    nurl = list(get_url(res, hDB))
                except Exception as e:
                    print("bs4 error :{}".format(e))
                    continue

                hDB.label_update(url)
                _new_url[0] += nurl[0]
                _new_url[1] += nurl[1]
            else:
            #200이 아닐 경우 bat_status.txt에 url과 응답 번호 저장
                #print("Status_Code is not 200: {} -> {}".format(url, res.status_code))
                hDB.insert_bad_url(url, "Status_Code", res.status_code)

        print("URL 수집 {}회 완료\t domain:{}\t url:{}\t{}".format(WholeCnt,_new_url[0],_new_url[1],datetime.datetime.now()))

        hDB.insert_log(-1, _new_url)
        WholeCnt += 1
    return

if __name__ == "__main__":
    hDB = DB_Handler()
    url = "http://dirnxxdraygbifgc.onion/"
    hDB.insert_domain_info(url)
    hDB.insert_domains(url)
    run()