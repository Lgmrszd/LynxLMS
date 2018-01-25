import urllib.parse as urlparse
from pg import DB


class LMSDB:
    def __init__(self, db_url):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(db_url)
        self.__db = DB(
            dbname=url.path[1:],
            user=url.username,
            passwd=url.password,
            host=url.hostname,
            port=url.port
        )

    def close(self):
        self.__db.close()