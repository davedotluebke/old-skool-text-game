#!/bin/bash

KEEP_GOING=0
until [ $KEEP_GOING -gt 0 ]
do
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
    myAddress="$(curl http://169.254.169.254/latest/meta-data/public-ipv4)"  # magic command for finding public IP of current instance
    python3 startup.py --server "$myAddress"
    KEEP_GOING=$?
done
