#!/bin/bash
cd /home/ubuntu/Code/bar-down-deals/scrapers/site_scraper 
export SCRAPY_PROJECT=default
~/.local/bin/poetry run python crawl.py > logs/crawl.log
