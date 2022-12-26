#!/bin/bash	

cd /game
# magic command for finding public IP of current instance	
myAddress="$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"  	
timeToReset="$((104378-$(date -d "1970-01-01 UTC $(date +%T)" +%s)))" # run until 22 seconds before the day ends
python3 startup.py --server "$myAddress" --mode "nocrypt" --duration "$timeToReset"
chgrp -R wizards saved_players
chmod -R ug+rw saved_players
