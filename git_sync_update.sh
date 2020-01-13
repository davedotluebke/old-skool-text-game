#!/bin/bash

cd /game

git fetch
git merge origin -m "Merged daily changes to GitHub with daily wizard updates." --no-edit
MERGE=$!

if [[ $MERGE -gt 0 ]]
then
	git reset --hard
fi
git push
