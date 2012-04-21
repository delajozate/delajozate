INSTALL
=======

Quick install guide::

  virtualenv --no-site-packages .
  . bin/activate
  hg clone https://bitbucket.org/samastur/delajozate
  pip install -r delajozate/requirements.txt
  pip install psycopg2
  cp delajozate/localsettings.py.example delajozate/localsettings.py
  python delajozate/manage.py syncdb
  python delajozate/manage.py migrate
  python delajozate/manage.py loaddata delajozate/fixtures/delajozate.json

