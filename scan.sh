#!/bin/sh

# now, just type command lines.

echo 'Install all the things!'
ls
cat /etc/passwd

source env/bin/activate
pip install -r requirements.txt
open http://localhost:5000/