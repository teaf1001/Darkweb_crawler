from pymongo import MongoClient
import tldextract as tld

my_client = MongoClient("mongodb://localhost:27017/")
DB = my_client["DBtest2"]
collection_domain_info = DB['domain_info']
collection_domains = DB['domains']
collection_badurl = DB['badurl']
collection_error = DB['error_log']

class domain():
    def __init__(self):
        self.domain = ''

    def insert_domains(self):
        return

    def insert_domain_info(self):
        return

    def insert_bad_domain(self):
        return

# db.classic.find({ "product_name": { $exists: true }} ) 필드가 존재하는지 여부 확인

# db.classic.findOne( { 'product_name': { $in: ['HHHHH'] }, 'product_category': { $in: ['TTTTTTTT'] } } )
# -> $in을 사용

# db.classic.findOne( { 'product_name': { $exists: true }, 'product_category': { $exists: true } } ) ->
# $exists를 사용하여 필드가 레코드에 존재하는지 여부를 확인

if __name__=="__main__":
    dict = {}
    with open("url.txt", "r+") as f:
        urls = f.readlines()
        for i in range(len(urls)):
            url = urls[i].replace("\n",'').replace('#','')
            extract = tld.extract(url)

            try:
                if extract.suffix != 'onion':
                    cause = 'suffix error'
                    print('suffix is not .onion : ', url)
                    post = {
                        "url": url,
                        'cause': cause
                    }
                    collection_badurl.insert(post)
                    # bad_url에 insert
                    continue

                if extract.domain == '':
                    cause = 'domain is not exist'
                    print('domain is not exist', url)
                    post = {
                        "url": url,
                        'cause': cause
                    }
                    collection_badurl.insert(post)
                    # bad_url에 insert
                    continue

                if type(collection_domains.find_one({"domain": extract.domain})) == type(dict):
                    post = {
                        "url": url,
                        "domain": extract.domain,
                        "sub_domain": extract.subdomain
                    }
                    collection_domain_info.insert(post)

                else:
                    post = {
                        "domain": extract.domain
                    }
                    collection_domains.insert(post)

                    post = {
                        "url": url,
                        "domain": extract.domain,
                        "sub_domain": extract.subdomain
                    }
                    collection_domain_info.insert(post)

            except Exception as e:
                post = {
                    "url": url,
                    "exception": e
                }
                collection_error.insert()
                pass

            # print(url)
            # post = {"url" : url,"sub_domain" : extract.subdomain, "domain" : extract.domain}
            # post = {"domain": extract.domain, "url": url}
            # collection_domains.insert(post)


            # print(extract)
            # print("subdomain:{}, domain:{}, suffix:{}".format(extract.subdomain, extract.domain, extract.suffix))

