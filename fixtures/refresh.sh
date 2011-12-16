#!/bin/bash

if [ ! -e manage.py ]; then
	echo "Run $0 from the directory containing manage.py!"
	exit 1
fi

python manage.py dumpdata --indent=4 --exclude south --exclude auth --exclude sessions --exclude admin --exclude contenttypes --exclude magnetogrami > fixtures/delajozate.json
