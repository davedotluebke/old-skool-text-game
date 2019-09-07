#!/bin/bash

KEEP_GOING=1
while [ $KEEP_GOING ]
do
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
    python3 startup.py
    $KEEP_GOING=$?
done
