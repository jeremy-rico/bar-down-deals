import logging

from api.src.aws.utils import get_ssm_param
from sqlalchemy import URL

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.src.spiders"]
NEWSPIDER_MODULE = "scraper.src.spiders"

# Database configuration
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=get_ssm_param("DB_USER", "postgres"),
    password=get_ssm_param("DB_PASSWORD", "", secure=True),
    host=get_ssm_param("DB_HOST", "localhost"),
    port=get_ssm_param("DB_PORT", "5432"),
    database=get_ssm_param("DB_NAME", "postgres"),
)

SCRAPERAPI_KEY = get_ssm_param("SCRAPERAPI_KEY", "", secure=True)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure the amount of time (in secs) that the downloader will wait before
# timing out (default: 180)
# DOWNLOAD_TIMEOUT = 30

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Retry Middleware
# RETRY_ENABLED = True
RETRY_TIMES = 5
# RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 418, 429]

# RANDOM_UA_PER_PROXY = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# NOTE: The integer value after each pipeline or middleware determine
# the order in which they run: items go through from lower valued to
# higher valued classes.

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "scraper.middlewares.WebScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# NOTE: Rotating user agents fixed 460 response
DOWNLOADER_MIDDLEWARES = {
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # "scraper.src.middlewares.ProxyRotationMiddleware": 350,
    # "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": 500,
    # "scraper.src.middlewares.WebScraperDownloaderMiddleware": 543,
    # "scraper.src.middlewares.ScraperApiProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scrapy.pipelines.images.ImagesPipeline": 1,
    "scraper.src.pipelines.PostgresPipeline": 300,
}
IMAGES_STORE = "s3://bar-down-deals-bucket/images/"

# AWS configuration
AWS_REGION = "us-west-1"
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

# Logger settings
BOTO_LOG_LEVEL = logging.CRITICAL  # logging.DEBUG

# Enable and configure the AutoThrottle extension
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
