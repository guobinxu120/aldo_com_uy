from requests import get
from parsel import Selector
from urlparse import urlparse

def get_categories():
    resp = get('http://www.aldo.com.uy/').text
    l = Selector(text=resp).xpath('//a[@class="item_submenu"]/@href').extract()
    return [urlparse(i).path for i in l]