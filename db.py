from pymongo import MongoClient
import tldextract as tld
import datetime
DB_Client = MongoClient("mongodb://localhost:27017/")
DB = DB_Client["DBtest100"]

#collection_domain_info = DB['domain_info'] # url, domain, sub_domain
#collection_domains = DB['domains'] # domain
#collection_badurl = DB['badurl'] # url, cause
#collection_error = DB['error_log'] # domain, error code, url
#collection_timeout = DB['timeout'] # domain, url


class domain:

    def __init__(self):
        self.url = ''
        self.cause = ''
        extract = tld.extract(self.url)

    def insert_domains(self, url):
        self.url = url
        extract = tld.extract(url)
        collection = DB['domains']
        post = {
            "domain": extract.domain
        }
        collection.insert_one(post)

    def insert_domain_info(self, url):
        self.url = url
        extract = tld.extract(url)
        collection = DB["domain_info"]
        if extract.subdomain !='':
            post = {
                "url": url,
                "domain": extract.domain,
                "sub_domain": extract.subdomain,
                "label": 0
            }
        else:
            post = {
                "url": url,
                "domain": extract.domain,
                "label": 0
            }
        collection.insert_one(post)

    def insert_bad_url(self, url, cause):
        self.url = url
        self.cause = cause
        collection = DB["bad_url"]
        post = {
            "url": url,
            'cause': cause
        }
        collection.insert_one(post)

    def insert_status_code(self, url, status_code):
        self.url = url
        collection = DB["status_code"]
        post = {
            "url" : url,
            "response_code" : status_code
        }
        collection.insert_one(post)

    def insert_error_log(self, url, exception):
        self.url = url
        collection = DB["error_log"]
        post = {
            "url" : url,
            "error_code": str(exception)
        }
        collection.insert_one(post)

    def insert_log(self, cnt):
        collection = DB["log"]
        post = {
            "log": "URL 수집 시작 {}회".format(cnt),
            "datetime": str(datetime.datetime.now())
        }
        collection.insert_one(post)

    def is_exist_domain(self, url):
        # Domains에 등록되어 있지 않음 -> domains와 domain_info에 둘다 추가
        self.url = url
        extract = tld.extract(url)

        try:
            if type(DB["domains"].find({"domain": extract.domain})[0]) == type(dict):
                return True
        except:
            return False

    def is_exist_url(self,url):
        # Domain_info에 등록되어 있지 않음 -> domain_info에 추가
        self.url = url
        extract = tld.extract(url)

        try:
            if type(DB["domain_info"].find({"domain": extract.domain})[0]) == type(dict):
                return True
        except:
            return False

    def label_update(self, url):
        self.url = url
        domain= tld.extract(url).domain
        DB['domain_info'].update_one({"domain": domain}, {"$set": {"label": 1}})
        return


def run(url_file):
    dict = {}
    with open(url_file, "r+") as f:
        urls = f.readlines()
        for i in range(len(urls)):
            url = urls[i].replace("\n", '').replace('#', '')
            extract = tld.extract(url)

            curl = domain()

            try:
                if extract.suffix != 'onion':
                    cause = 'suffix error'
                    print('suffix is not .onion : ', url)
                    curl.insert_bad_url(url, cause)
                    continue

                if extract.domain == '':
                    cause = 'domain is not exist'
                    print('domain is not exist', url)
                    curl.insert_bad_url(url, cause)
                    continue

                try:
                    if type(DB["domains"].find({"domain": extract.domain})[0]) == type(dict):
                        #domains에 등록되어 있는 지
                        try:
                            if type(DB["domain_info"].find({"domain": extract.domain})[0]) == type(dict):
                                #domain_info에 등록되어 있음 -> continue
                                continue
                        except:
                            #domain_info에 등록되어 있지 않음 -> domain_info에 등록
                            curl.insert_domain_info(url)

                except:
                    #Domains에 등록되어 있지 않음 -> domains와 domain_info에 둘다 추가
                    curl.insert_domains(url)
                    curl.insert_domain_info(url)

            except Exception as e:
                #기타 에러
                print('DB insert error:', e)
                post = {
                    "url": url,
                    "exception": e
                }
                curl.insert_error_log(url, e)
                pass

if __name__ == "__main__":
    Cdomain = domain()
    url = "http://wikitjerrta4qgz4.onion/"
    Cdomain.insert_domain_info(url)
    Cdomain.insert_domains(url)
    #file = 'url.txt'
    #run(file)