#!/bin/bash

while :
do
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
    python3 startup.py
done
