#!/bin/bash
cd /home/ec2-user/Projects/bar-down-deals/alerts/src 
~/.local/bin/poetry run python main.py -f daily > logs/daily.log
