#!/bin/sh
python3 -m http.server 8000 &
python3 OAD.py
kill $!
