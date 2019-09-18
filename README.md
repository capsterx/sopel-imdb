Sopel IMDB
===========================

IMDB module for Sopel IRC bot framework

Requirements
------------

* Sopel 6+
* python 3.6+

Installation
------------

The only supported installation method is via ``pip3``::

    pip3 install https://github.com/capsterx/sopel-imdb.git@master

Also to upgrade to the latest code, do::

    pip3 install --upgrade git+https://github.com/capsterx/sopel-imdb.git@master

Configuration
-------------

Required
::::::::

The IMDB API requires a key to be added in the bot’s config. 
Sign up for API at http://www.omdbapi.com/  or https://rapidapi.com/imdb/api/movie-database-imdb-alternative
and add it to your sopel config

::

    [movies]
    rapid_api_key = yourappidgoeshere
    omdb_api_key = yourappidgoeshere
    api_type = omdb or rapid

You can also do:
`sopel --configure-modules`
and select `y` for `movies`

Usage
-----

::

    <User> .imdb <search>

A Note About Reloading
----------------------

In versions of sopel up to 6.5.0 (the last tested version), reloading a third-party module
installed from pip, such as wolfram, results in duplicated output. This is `a known issue in
sopel <https://github.com/sopel-irc/sopel/issues/1056>`_ and is being worked on.

**Workaround:** After updating sopel-imdb through pip3, restart the bot at your earliest
convenience to enable the latest code.

Support
-------
