import urllib.parse as urlparse
from pg import DB

class LMSDB:
    def __init__(self, db_url):
        urlparse.uses_netloc.append("postgres")
        self.__db_url = db_url
        url = urlparse.urlparse(db_url)
        self.__db = DB(
            dbname=url.path[1:],
            user=url.username,
            passwd=url.password,
            host=url.hostname,
            port=url.port
        )
