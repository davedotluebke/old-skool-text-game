#!/bin/bash

while :
do
    git add -A
    git commit -m "Daily commit to add wizard-generated files to GitHub."
    git pull
    FAIL=$?
    if ((FAIL))
    then
        git reset --hard
        echo "Merge conflict occured."
    else
        git push
        echo "No merge conflicts."
    fi
    python3 startup.py
done
