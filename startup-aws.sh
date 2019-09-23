#!/bin/bash

KEEP_GOING=0
until [ $KEEP_GOING -gt 0 ]
do

    myAddress="$(curl -s http://169.254.169.254/latest/meta-data/hostname)"  # magic command for finding public IP of current instance
    python3 startup.py --server "$myAddress"
    KEEP_GOING=$?
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
done
