#!/bin/bash
cd /home/ec2-user/Projects/bar-down-deals/scrapers/stick_scraper 
export SCRAPY_PROJECT=sticks
~/.local/bin/poetry run python crawl.py > logs/crawl.log
