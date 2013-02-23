#!/bin/bash

DUMPFILE=delajozate_latest.pgsql

scp delajozate@delajozate.si:~/dumps/$DUMPFILE .

/usr/lib/postgresql/9.2/bin/pg_restore --no-owner -p 5433 -d delajozate $DUMPFILE


