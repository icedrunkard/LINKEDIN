# -*- coding: utf-8 -*-

# Scrapy settings for googles project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'googles'

SPIDER_MODULES = ['googles.spiders']
NEWSPIDER_MODULE = 'googles.spiders'
MONGO_HOST = 'localhost:27777'
#MONGO_DATABASE = 'BUAA'
#COLLECTION_NAME='化学学院'

SCHOOL_LIST=[
    'RENMIN',
   #           'BIT','PKU','XMU','SJTU','ZJU','FUDAN','BNU','BUAA','TONGJI',
    #          'THU',
              ]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'googles (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False


# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0.2

#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#REDIS_URL = 'redis://localhost:6379/1'

#以下设置广度优先
#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'



RETRY_TIMES=30
RETRY_HTTP_CODES=[302,400,401,402,403,408,503,999]
DOWNLOAD_TIMEOUT=10

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 15

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16



# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Encoding':'gzip, deflate, sdchAccept-Encoding:gzip, deflate, sdch',
#    'Accept-Language':'zh-CN,zh;q=0.8',
#    'Upgrade-Insecure-Requests':'1',
#    'Cache-Control':'max-age=0',
#    'Connection':'keep-alive',
#'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',  
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'googles.middlewares.GooglesSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'scrapy.downloadermiddlewares.useragent.HttpAuthMiddleware':None,
#    'googles.middlewares.AuthMiddleware':50,
#    'googles.middlewares.AbuyunProxiesMiddleware': 543,
#    'googles.middlewares.VPSProxiesMiddleware': 544,
     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#    'googles.middlewares.ReMiddleware': 90,
#    'googles.middlewares.RotateUserAgentMiddleware': 400,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'googles.pipelines.MongoPipeline': 300,
     'googles.pipelines.MongoNewPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
