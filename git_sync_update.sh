#!/bin/hash
git fetch
git merge origin -m "Merged daily changes to GitHub with daily wizard updates." --no-edit
MERGE = $!

if [MERGE]:
	git reset --hard
