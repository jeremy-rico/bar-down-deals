#!/bin/bash
cd /home/ubuntu/Code/bar-down-deals/alerts/src 
~/.local/bin/poetry run python main.py -f weekly> ../logs/weekly.log
