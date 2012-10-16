INSTALL
=======

Quick install guide::

  hg clone https://bitbucket.org/samastur/delajozate
  python bootstrap.py -d
  bin/buildout

  cp delajozate/localsettings.py.example delajozate/localsettings.py
  python delajozate/manage.py syncdb
  python delajozate/manage.py migrate
  python delajozate/manage.py loaddata delajozate/fixtures/delajozate.json
