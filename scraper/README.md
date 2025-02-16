# Web Scraper

## Description

## List of sites scraped

## NOTES

### psycopg2 install

Scraper uses psycopg2 as a backend for sqlmodels. It does not do async writes to
the DB like api does. Thereofre it needs to dependencies to install psycopg2

1. python headers
2. libq headers

They can be installed with the following line;
For AL2023

```bash
sudo dnf install libpq-dev python3-devel
```

For other distros and docker see the [psycopg2 docs](https://www.psycopg.org/docs/install.html)

### Editing pythonpath in venv for neovim lspconfig

Scrapy's root directory is at ../../bar-down-deals since that's where scrapy.cfg
is located. This gives scrapy access to modules in the api project. Therefore
imports in this project will need to look like this

```python3
from api.src.deals.models import Deals
from api.src.core import get_session
```

For production you have nothing to worry about. HOWEVER, for development, if you
want you IDE and lsp to be able to resolve these imports, you will need to add
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
echo path/to/bar/down/deals/project >> bardowndeals.path
```

4. restart your venv

This now matches the production environment where scrapy will put the root
python directory to wherever the location of scrapy.cfg is.
