class Movies:
    def __init__(self, api):
        #self.imdb = rapidapi.Imdb(rapid_host, rapid_key)
        self.imdb = api

    def _format_long(self, m):
        return f"{m['Title']} | {m['Year']} | {m['Rated']} | {m['Released']} | {m['imdbRating']}/10 | {m['Plot']} | https://www.imdb.com/title/{m['imdbID']}"

    def _format_short(self, i):
        return f"{i['Title']}/{i['Year']}/{i['Type']}"

    def _format_group(self, response):
        return ', '.join([self._format_short(x) for x in response["Search"]])

    def _good_enough(self, text, year, result):
        a = [x for x in result["Search"] if x['Title'].lower() == text.lower() and str(x['Year']) == str(year)]
        if len(a) == 1:
            return a[0]
        else:
            return None

    def _filter_duplicates(self, result):
        #There has to be a better way to filter this
        #but sometimes it returns duplicated results
        if 'Search' in result:
          seen = set()
          def is_in(x):
              r=x['imdbID'] in seen
              if not r:
                  seen.add(x['imdbID'])
              return not r
          result['Search'] = list(filter(is_in, result['Search']))
          result['totalResults'] = str(len(result['Search']))

    def _found_single_match(self, result):
        return 'totalResults' in result and int(result["totalResults"]) == 1

    def _lookup(self, text, year=None):
        result = self.imdb.search(text, year)
        self._filter_duplicates(result)

        if self._found_single_match(result):
           return self._format_long(self.imdb.get_by_id(result["Search"][0]["imdbID"]))

        if year is None:
            try:
                a = text.split()
                year = int(a[-1])
                return self._lookup(text[0:-(len(a[-1])+1)], year)
            except Exception as e:
                pass
        else:
            r = self._good_enough(text, year, result)
            if r:
                return self._format_long(self.imdb.get_by_id(r["imdbID"]))
        
        if 'Error' in result:
            return result['Error']

        return self._format_group(result)

    def lookup(self, text):
        return self._lookup(text)

if __name__ == "__main__":
    from . import config
    import sys
    if config.api_type == "omdb":
        from . import omdbapi
        api = omdbapi.Imdb(
              config.omdb_api_host,
              config.omdb_api_key)
    else:
        from . import rapidapi
        api = rapidapi.Imdb(
              config.rapid_api_host,
              config.rapid_api_key)
    movies = Movies(api)
    print(movies.lookup(sys.argv[1]))
