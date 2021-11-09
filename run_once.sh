#!/bin/bash	

cd /game
# magic command for finding public IP of current instance	
myAddress="$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"  	
python3 startup.py --server "$myAddress" --mode "nocrypt" --duration 86398  # run for 1 day less 2 minutes	
chgrp -R wizards saved_players
chmod -R ug+rw saved_players
