#!/bin/bash

KEEP_GOING=0
until [ $KEEP_GOING -gt 0 ]
do
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
    $KEEP_GOING=$(python3 startup.py)
done
