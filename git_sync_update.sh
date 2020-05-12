#!/bin/bash

cd /game

if pgrep python3; then killall python3; fi

git fetch
git merge origin -m "Merged daily changes to GitHub with daily wizard updates." --no-edit
chgrp gameadmins *.py
chgrp -R wizards domains
chgrp -R wizards home
chgrp -R wizards saved_players
chgrp wizards backup_saved_players/*.OADplayer
chgrp -R wizards potions
chgrp -R currencies currencies
MERGE=$!

if [[ $MERGE -gt 0 ]]
then
	git reset --hard
fi
git push

python3 gitbot_committer.py
