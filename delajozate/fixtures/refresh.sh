#!/bin/bash

if [ ! -e manage.py ]; then
	echo "Run $0 from the directory containing manage.py!"
	exit 1
fi

echo -n "Did you patch Django's dumpdata? y/n "
read django_patched

if [ "$django_patched" != "y" ]
then
	echo ""
	echo " Please add .order_by('pk') to Django's dumpdata script"
	echo " in django/core/management/commands/dumpdata.py,"
	echo " lines 108 and 110 (Django 1.3)"
	echo " This is needed to ensure stable sort and readable diff."
	exit 1
fi


python manage.py dumpdata --indent=4 --exclude south --exclude auth --exclude sessions --exclude admin --exclude contenttypes \
	--exclude magnetogrami.Video \
	--exclude magnetogrami.Glasovanje \
	--exclude magnetogrami.Glas \
	--exclude magnetogrami.Seja \
	--exclude magnetogrami.Zasedanje \
	--exclude magnetogrami.Zapis > fixtures/delajozate.json
