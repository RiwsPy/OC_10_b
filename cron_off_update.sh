#!/bin/bash
echo "db OFF update"
pipenv shell
./manage.py uDB
echo "end of update"
