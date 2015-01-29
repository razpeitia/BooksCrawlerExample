# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from Book.items import BookItem

class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["casadellibro.com"]
    start_urls = (
        'http://www.casadellibro.com/busqueda-generica',
    )
    rules = (
        Rule(
            LxmlLinkExtractor(
                restrict_xpaths='//a[@class="gonext"]'
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = BookItem()
        for eitem in response.xpath('//div[@class="mod-list-item"]'):
            item['title'] = ''.join(eitem.xpath('.//a[@class="title-link"]/text()').extract())
            item['description'] = ''.join(eitem.xpath('.//p[@class="smaller pb15"]/text()').extract())
            item['price'] = ''.join(eitem.xpath('.//p[@class="currentPrice"]/text()').extract())
            yield item
