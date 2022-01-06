import scrapy

from urlparse import urlparse


class CategoriesOfAldoComUy(scrapy.Spider):

    name = "categories_of_aldo_com_uy"
    start_urls = ('https://empresas.aldo.com.uy/',)

    def parse(self, response):
        l = response.xpath('//a[@class="main-menu-column__link"]/@href').extract()
        yield {'links': [urlparse(i).path for i in l]}
