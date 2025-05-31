# Web Scrapers

## Description

The scrapers for BarDownDeals. Consists of two projects.

1. Site Scraper: Scrapes all deals (not apparel) from all sites.
2. Stick Scraper: Looks for only certain sticks on all sites to track historical
   price

## List of sites scraped

## NOTES

### Editing pythonpath in venv for neovim lspconfig

Scrapy's root directory is at /bar-down-deals since that's where scrapy.cfg
is located. This gives scrapy access to modules in the api project. Therefore
imports in this project will need to look like this

```python3
from api.src.deals.models import Deals
from api.src.core import get_session
```

For production you have nothing to worry about. HOWEVER, for development, if you
want your IDE and lsp to be able to resolve these imports, you will need to add
the bar_down_deals root directory to the python path.

There are many ways to do this, but I've found the best to be by adding a .pth
file to the venv site-packages directory.

1. After activating your env, find its location with

```bash
poetry env info
```

2. Navigate to the env's site-packages directory

```bash
cd <env_path>/lib/python3.11/site-packages/
```

3. add a new .pth file (any name is fine) with the absolute path to the
   bar_down_deals root inside of it

```bash
echo path/to/bar/down/deals/project >> bardowndeals.pth
```

4. restart your venv

This now matches the production environment where scrapy will put the root
python directory to wherever the location of scrapy.cfg is.
