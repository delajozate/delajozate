#!/bin/bash

echo "Add following line to your localsettings.py:"
echo "HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr/delajozate'"

ssh -L 8080:127.0.0.1:8080 delajozate@delajozate.si

