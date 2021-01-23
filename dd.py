import requests
import os
from bs4 import BeautifulSoup
import datetime
import tldextract as tld
import time

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

numberof_url = 0

def web_parser(url, res):
    # 수정하기 : 파일 이름 도메인 + 서픽스로 하지 말고 http://만 빼고 다 작성하기 -> 모든 페이지 대상
    # save html code as a file
    # name 변수 정규식으로 걸러내기
    #name = url.replace('https://','').replace('http://','').replace('/', '').replace('\\', '').replace('?', '').replace(':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '')
    extract = tld.extract(url)
    name = "{}.{}".format(extract.domain, extract.suffix)
    path = os.getcwd() + '\\web\\' + name
    with open(path, 'a+', encoding='utf8') as f:
        try:
            f.write(url + '\n')
            f.write(res.text)
        except Exception as e:
            print("FILE CREATE ERROR -> ", e)
    print("Web Parse Success -> ", url)
    return

def get_url(url, res):
    global numberof_url
    # extract new domain in a website
    disasm_url = tld.extract(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    with open('new.txt', 'a+') as f:
        with open('total_url.txt', 'a+') as p:
            for a in soup.find_all('a', href=True):
                if int('.onion' in a['href']) & int('http' in a['href']) & int(disasm_url.domain not in a['href']): #
                    f.write(a['href'] + "\n")
                    p.write(a['href'] + "\n")
                    numberof_url += 1
    return

#def find_url(path):

def run(url_file):
    cnt = 0
    total = 0
    while(1):
        global numberof_url
        numberof_url = 0
        parsed = 0

        log = 'URL 수집 시작 {}회\t {} \n'.format(cnt, datetime.datetime.now())
        print(log)

        with open('log.txt', 'a+') as log_txt:
            log_txt.write(log)

        #url 배열로 받아오기
        with open(url_file, 'r+') as f:
            urls = f.readlines()

        for i in range(len(urls)):
            url = urls[i].replace('\n', '')
            #url 응답 보내기
            try:
                res = requests.get(url, proxies=proxies, timeout=10)
            except Exception as e:
                print("Request Timeout   -> ", url)
                with open("pass.txt", 'a+') as p:
                    p.write(url + '\n')
                continue

            #정상 응답일 경우 해당 url의 html code 및 추가 url 파싱
            if res.status_code == 200:
                web_parser(url, res)
                parsed += 1
                get_url(url, res)
            else:
            #200이 아닐 경우 bat_status.txt에 url과 응답 번호 저장
                print("response status code is not 200: {} -> {}".format(url, res.status_code))
                with open('bad_status.txt', 'a+') as badurl:
                    badurl.write("{} -> {}\n".format(url, res.status_code))

        #새로운 url 저장 마쳤으면 기존 url 텍스트 파일 내용 비우기
        with open('url.txt', 'w') as old:
            print('url.txt 내용 비우기 완료')
            with open('new.txt', 'r') as new:
                old.write(new.read())
                print('new.txt에 새로운 url 작성 완료')

        open('new.txt', 'w')
        print('new.txt 내용 비우기 완료')
        print("URL 수집 완료\t", datetime.datetime.now())

        with open('log.txt', 'a+') as log_txt:
            log = 'URL {}개 파싱\n새 도메인 {}개 등록 완료\n\n'.format(parsed, numberof_url)
            total += numberof_url
            print(log)
            print("수집한 총 url: {}개".format(total))
            log_txt.write(log)

        cnt += 1
    return

if __name__=="__main__":
    url_file = 'url.txt'
    run(url_file)