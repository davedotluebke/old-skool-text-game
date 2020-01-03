#!/bin/bash	

# magic command for finding public IP of current instance	
myAddress="$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"  	
python3 startup.py --server "$myAddress" --mode "encrypt" --duration 86398  # run for 1 day less 2 minutes	

