#!/bin/bash

# magic command for finding public IP of current instance
echo "Hello world!"
myAddress="$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"  
python3 /game/startup.py --server "$myAddress" --mode "encrypt" --duration 60  # run for one minute then shut down
