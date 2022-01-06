# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import TextResponse
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
#from scrapy.utils.response import open_in_browser
#from scrapy.shell import inspect_response

from urlparse import urlparse
from json import loads
from datetime import date
import time
import datetime


class AldoComUySpider(scrapy.Spider):

    name = "aldo_com_uy_spider"

###########################################################

    def __init__(self, categories=None, *args, **kwargs):
        super(AldoComUySpider, self).__init__(*args, **kwargs)

        if not categories:
            raise CloseSpider('Received no categories!')
            #self.start_urls = ["/papeleria/archivo-y-clasificacion/archivadores"]
        else:
            self.categories = categories
            links = loads(self.categories)
            self.start_urls = links.keys()
        

        # shortcut func for extract the product field
        self.fld = lambda s, x: s.xpath(x).extract_first()

    def start_requests(self):
        for l in self.start_urls:
            url = 'https://empresas.aldo.com.uy{}'.format(l)
            if 'https:' in l:
                url = l
            yield scrapy.Request(url, meta={'CatURL': l, 'nextCount': 1})

###########################################################

    def parse(self, response):

        #open_in_browser(response)
        #inspect_response(response, self)

        new_resp = response
        if response.meta['nextCount'] > 1:
            try:
                json_data = loads(response.body)['product_datagrid']
                new_resp = TextResponse(url=response.url,
                                body=json_data,
                                encoding='utf-8')
                i = 0
            except:
                return
        products = new_resp.xpath('//div[@data-layout-model="productModel"]')
        if not products:
            return

        for tag in products:
            item = {}

            item['Vendedor'] = 256
            # item['ID'] = self.fld(i, './div[2]/a/strong/text()')
            item['ID'] = tag.xpath('.//*[@class="sku"]/text()').re('[\d,]+')[0]

            # item['Title'] = self.fld(i, './div[3]/a/text()')
            item['Title'] = tag.xpath('.//*[@class="view-product"]/text()').extract_first().strip()

            # item['Description'] = self.fld(i, './div[4]/text()')
            try:
                item['Description'] = ''.join(tag.xpath('.//*[@class=" product__description product__description_gallery-view"]//*/text()').extract_first()).strip()
            except:
                item['Description'] = ""
                #open_in_browser(response)
                #inspect_response(response, self)
            integer = tag.xpath('.//*[@class="unit"]/text()').re('[\d.]+')[0].replace('.', '')
            decimal = tag.xpath('.//*[@class="decimal"]/text()').extract_first().strip()
            price = ''
            if decimal:
                price = integer + '.' + decimal
            else:
                price = integer
            item['Price'] = price
            item['Currency'] = 'UYU'

            item['Category URL'] = response.meta['CatURL']
            item['Details URL'] = response.urljoin(tag.xpath('.//*[@class="view-product"]/@href').extract_first())
            item['Date'] = date.today()

            item['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            item['image_url'] = response.urljoin(tag.xpath('.//*[@class="view-product"]/@style').extract_first().split("background-image: url('")[-1].split("'")[0])

            yield item

        response.meta['nextCount'] += 1
        next_page_url = response.urljoin(response.meta['CatURL']) + "?frontend-product-search-grid%5BincludeSubcategories%5D=1&frontend-product-search-grid%5BoriginalRoute%5D=oro_product_frontend_product_index&appearanceType=grid&frontend-product-search-grid%5B_pager%5D%5B_page%5D={}&frontend-product-search-grid%5B_pager%5D%5B_per_page%5D=24&frontend-product-search-grid%5B_parameters%5D%5Bview%5D=__all__&frontend-product-search-grid%5B_appearance%5D%5B_type%5D=grid&layout_block_ids%5B%5D=product_datagrid".format(str(response.meta['nextCount']))

        # '//img[@title="Siguiente"]/parent::a/@href')
        # next_page_url = response.xpath('//*[@class="btn btn--size-s btn--default oro-pagination__next"]')
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url),
                                 meta=response.meta)
