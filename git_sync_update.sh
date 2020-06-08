#!/bin/bash

cd /game

if pgrep python3; then killall python3; fi

git fetch
git merge origin -m "Merged daily changes to GitHub with daily wizard updates." --no-edit
chgrp gameadmins *.py
chgrp -R wizards domains home saved_players potions currencies game_log.txt
chgrp wizards backup_saved_players/*.OADplayer
MERGE=$!

if [[ $MERGE -gt 0 ]]
then
	git reset --hard
fi
git push

python3 gitbot_committer.py
