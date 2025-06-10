#!/bin/bash
cd /home/ubuntu/Code/bar-down-deals/alerts/src 
~/.local/bin/poetry run python main.py -f daily > ../logs/daily.log
