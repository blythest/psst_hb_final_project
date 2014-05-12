#!/bin/sh

echo 'Install all the things!'


virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
python views.py &
open 'http://localhost:5000/'