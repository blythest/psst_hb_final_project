#!/bin/sh

# now, just type command lines.

echo 'Install all the things!'
ls
cat /etc/passwd

virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
python views.py
open http://localhost:5000