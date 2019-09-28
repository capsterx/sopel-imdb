import requests
import json

class Imdb:
    def __init__(self, host, key):
        self.host = host
        self.key = key

    @property
    def url(self):
        return f"https://{self.host}/"

    @property
    def headers(self):
        return {}

    def querystring(self, search, year=None, typ=None):
        d = {"page":"1","r":"json","s": search, 'apikey': self.key}
        if year:
            d['y'] = str(year)
        if typ:
            d['type'] = typ
        return d

    def search(self, search, year=None, typ=None):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring(search, year, typ))
        return json.loads(response.text)

    def get_by_id(self, imdbID):
        response = requests.request("GET", self.url, headers=self.headers, params={"i":imdbID, 'apikey': self.key})
        return json.loads(response.text)
