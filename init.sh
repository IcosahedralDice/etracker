#!/bin/bash


mkdir -p data/
echo 'Creating database data/data.db'
sqlite3 data/test.db < schema.sql
echo 'Database created'
