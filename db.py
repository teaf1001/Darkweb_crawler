from pymongo import MongoClient
import tldextract as tld
import datetime

class DB_Handler:

    def __init__(self):
        self.cause = ''
        self.DB_Client = MongoClient("mongodb://localhost:27017/")
        self.DB = self.DB_Client["d41"]

    def insert_domains(self, url):
        extract = tld.extract(url)
        collection = self.DB['domains']
        post = {
            "domain": extract.domain
        }
        collection.insert_one(post)

    def insert_domain_info(self, url):
        extract = tld.extract(url)
        collection = self.DB["domain_info"]
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

    def insert_bad_url(self, url, cause, status_code):
        self.cause = cause
        collection = self.DB["bad_url"]
        if cause == 'status_code':
            post = {
                "url": url,
                'cause': cause
            }
            collection.insert_one(post)
            self.label_update(url)
        else:
            post = {
                "url": url,
                'cause': cause,
                'status_code': status_code
            }
            collection.insert_one(post)
            self.label_update(url)


    def insert_log(self, cnt):
        collection = self.DB["log"]
        post = {
            "log": "URL 수집 시작",
            "count": cnt,
            "datetime": str(datetime.datetime.now())
        }
        collection.insert_one(post)

    def is_exist_domain(self, url):
        extract = tld.extract(url)
        if str(self.DB["domains"].find_one({"domain": extract.domain})) != "None":
            return True
        else:
            return False

    def is_exist_url(self, url):
        collection = self.DB['domain_info']
        if str(collection.find_one({"url": url})) != "None":
            return True
        else:
            return False

    def label_update(self, url):
        self.DB['domain_info'].update_many({"url": url}, {"$set": {"label": 1}})
        return


def run(url_file):
    dict = {}
    with open(url_file, "r+") as f:
        urls = f.readlines()
        for i in range(len(urls)):
            url = urls[i].replace("\n", '').replace('#', '')
            extract = tld.extract(url)
            curl = DB_Handler()



if __name__ == "__main__":
    hDB = DB_Handler()
    url = "http://dirnxxdraygbifgc.onion/"
    hDB.insert_domain_info(url)
    hDB.insert_domains(url)
    #file = 'url.txt'
    #run(file)