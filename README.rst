INSTALL
=======

Quick install guide::

  # libpq needed for psycopg2 (Linux)
  sudo apt-get install libpq-dev python-dev build-essential

  # create a virtualenv in containing dir
  mkdir dz && cd dz
  virtualenv .

  # clone code
  git clone https://github.com/delajozate/delajozate.git

  # activate virtualenv
  . bin/activate
  cd delajozate
  
  # setup buildout
  python bootstrap.py -d
  bin/buildout

  # setup settings, database
  cp delajozate/localsettings.py.example delajozate/localsettings.py
  
  # create database
  # NOTE: for collation to work, you need to
  # have appropriate locales generated locally.
  createdb -E utf-8 -O `whoami` --lc-collate=sl_SI.UTF-8 --lc-ctype=sl_SI.UTF-8 -T template0 delajozate
  
  # fill database
  bin/django syncdb
  bin/django migrate
  bin/django loaddata delajozate/fixtures/delajozate.json

  # run
  bin/django runserver

TODO
====

Setup crontab for bin/django twitter_sync every 30min
