from pymongo import MongoClient
import tldextract as tld
import datetime

class DB_Handler:

    def __init__(self):
        self.DB_Client = MongoClient("mongodb://localhost:27017/")
        self.dbname = "d16"
        self.DB = self.DB_Client[self.dbname]

    def insert_domain(self, url):
        if not self.is_exist_url(url, 'Domain'):
            extract = tld.extract(url)
            collection = self.DB['Domain']
            post = {
                "Domain": extract.domain
            }
            collection.insert_one(post)
            self.insert_domain_info(url)
            return 1
        elif not self.is_exist_url(url, 'Domain_Info'):
            self.insert_domain_info(url)
            return 2


    def insert_domain_info(self, url):
        extract = tld.extract(url)
        collection = self.DB["Domain_Info"]
        if extract.subdomain !='':
            post = {
                "Url": url,
                "Domain": extract.domain,
                "Sub_domain": extract.subdomain,
                "Label": 0
            }
        else:
            post = {
                "Url": url,
                "Domain": extract.domain,
                "Label": 0
            }
        collection.insert_one(post)

    def insert_bad_url(self, url, cause, status_code):
        collection = self.DB["Bad_Url"]
        if cause == 'Status_Code':
            post = {
                "Url": url,
                'Cause': cause,
                'Status_Code': status_code
            }
            collection.insert_one(post)
            self.label_update(url)
        else:
            post = {
                "Url": url,
                'Cause': cause,
            }
            collection.insert_one(post)
            self.label_update(url)

    def insert_log(self, cnt, new_url_tuple):
        collection = self.DB["Log"]
        if cnt != -1:
            post = {
                "Log": "URL 수집 시작: {}회".format(cnt),
                "Datetime": str(datetime.datetime.now()),
            }
            collection.insert_one(post)
        else:
            post = {
                "Log": "URL 수집 끝",
                "Datetime": str(datetime.datetime.now()),
                "New_domain": new_url_tuple[0],
                "New_url": new_url_tuple[1]
            }
            collection.insert_one(post)

    def is_exist_url(self, url, collection):
        if collection == 'Domain':
            collection = self.DB[collection]
            extract = tld.extract(url)
            if str(collection.find_one({"Domain": extract.domain})) != "None":
                return True
            else:
                return False

        elif (collection == 'Domain_Info') or (collection == 'Bad_Url'):
            collection = self.DB[collection]
            if str(collection.find_one({"Url": url})) != "None":
                return True
            else:
                return False
        else:
            print("is_exist_url Unexpected Result-: Url:{}".format(url), collection)
            return

    def label_update(self, url):
        self.DB['Domain_Info'].update_many({"Url": url}, {"$set": {"Label": 1}})
        return