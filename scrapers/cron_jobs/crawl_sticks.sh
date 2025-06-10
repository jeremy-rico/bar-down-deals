#!/bin/bash
cd /home/ubuntu/Code/bar-down-deals/scrapers/stick_scraper 
export SCRAPY_PROJECT=sticks
~/.local/bin/poetry run python crawl.py > logs/crawl.log
