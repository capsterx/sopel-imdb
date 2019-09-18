from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import commands, example
from sopel import web
from .imdb import Movies

class MoviesSection(StaticSection):
    rapid_api_host = ValidatedAttribute('rapid_api_host', default="movie-database-imdb-alternative.p.rapidapi.com")
    rapid_api_key = ValidatedAttribute('rapid_api_key', default=None)
    omdb_api_host = ValidatedAttribute('omdb_api_host', default="www.omdbapi.com")
    omdb_api_key = ValidatedAttribute('omdb_api_key', default=None)
    api_type = ChoiceAttribute('api_type', choices=['omdb', 'rapid'], default='omdb')


def configure(config):
    config.define_section('movies', MoviesSection, validate=False)
    config.movies.configure_setting('rapid_api_host', 'rapidapi.com host')
    config.movies.configure_setting('rapid_api_key', 'rapidapi.com key')
    config.movies.configure_setting('omdb_api_host', 'omdbdapi.com host')
    config.movies.configure_setting('omdb_api_key', 'omdbdapi.com key')
    config.movies.configure_setting('api_type', 'omdb | rapid')

def setup(bot):
    bot.config.define_section('movies', MoviesSection)

def check(bot, trigger):
  msg = None
  if not bot.config.movies.api_type:
      msg = 'Movies API type not configured'
  else:
    if bot.config.movies.api_type == "rapid":
      if not bot.config.movies.rapid_api_host:
          msg = 'Movies API rapidapi.com host not configured.'
      elif not bot.config.movies.rapid_api_key:
          msg = 'Movies API rapidapi.com key not configured.'
    else:
      if not bot.config.movies.omdb_api_host:
          msg = 'Movies API omdbapi.com host not configured.'
      elif not bot.config.movies.omdb_api_key:
          msg = 'Movies API omdbapi.com key not configured.'
  if not msg and not trigger.group(2):
      msg = 'You must provide a query.'
  return msg

import sopel.module
@sopel.module.commands('imdb')
@sopel.module.example('.imdb beta test')
@sopel.module.example('.imdb beta test 2016')
def get_imdb(bot, trigger):
  msg = check(bot, trigger)
  if not msg:
      if bot.config.movies.api_type == "omdb":
        from . import omdbapi
        api = omdbapi.Imdb(
              bot.config.movies.omdb_api_host,
              bot.config.movies.omdb_api_key)
      else:
        from . import rapidapi
        api = rapidapi.Imdb(
              bot.config.movies.rapid_api_host,
              bot.config.movies.rapid_api_key)

      movies = Movies(api)
      msg = movies.lookup(trigger.group(2))
  bot.say(msg)
