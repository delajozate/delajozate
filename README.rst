INSTALL
=======

* virtualenv --no-site-packages .
* . bin/activate
* pip install -r requirements.txt
* pip install psycopg2
* vim hrcek/settings.py # insert: from devsettings import \*, setup DATABASES
* hrcek/manage.py syncdb

