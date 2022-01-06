# -*- coding: utf-8 -*-
BOT_NAME = 'aldo_com_uy'
SPIDER_MODULES = ['aldo_com_uy.spiders']
NEWSPIDER_MODULE = 'aldo_com_uy.spiders'

USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
COOKIES_ENABLED = False

CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.5
