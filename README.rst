INSTALL
=======

Quick install guide::

  # libpq needed for psycopg2 (Linux)
  sudo apt-get install libpq-dev

  # create a virtualenv in containing dir
  mkdir dz && cd dz
  virtualenv .

  # clone code
  hg clone https://bitbucket.org/samastur/delajozate

  # activate virtualenv
  . bin/activate
  cd delajozate
  
  # setup buildout
  python bootstrap.py -d
  bin/buildout

  # setup settings, database
  cp delajozate/localsettings.py.example delajozate/localsettings.py
  
  # fill database
  bin/django syncdb
  bin/django migrate
  bin/django loaddata delajozate/fixtures/delajozate.json

  # run
  bin/django runserver

TODO
====

Setup crontab for bin/django twitter_sync every 30min
