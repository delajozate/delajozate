INSTALL
=======

* virtualenv --no-site-packages .
* . bin/activate
* pip install -r requirements.txt
* pip install psycopg2
* vim localsettings.py
* ./manage.py syncdb
* ./manage.py migrate
* ./manage.py loaddata fixtures/delajozate.json

