#!/bin/bash
cd /home/ec2-user/Projects/bar-down-deals/scrapers/site_scraper 
export SCRAPY_PROJECT=default
~/.local/bin/poetry run python crawl.py > logs/crawl.log
