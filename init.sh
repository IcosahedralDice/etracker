#!/bin/bash


mkdir -p data/
echo 'Creating database data/test.db'
sqlite3 data/test.db < schema.sql
echo 'Database created'
