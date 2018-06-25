# -*- coding: utf-8 -*-
import scrapy


class MetropolitonSpider(scrapy.Spider):
    name = 'metropoliton'
    allowed_domains = ['mcentre.lk']
    start_urls = ['http://mcentre.lk/']

    def parse(self, response):
        link_path = '//div[@class="no_blink_cls"]/\
                div[not(@class="menu4")and@class="menu parrent-arrow"]//\
                a/@href'
        links =  response.selector.xpath(link_path).extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_products_page)
            

    def parse_products_page(self, response):
        prod_link_path = '//h2[@class="product-name"]/a/@href'
        nxt_link_path = '/a[@title="Next"]/@href'
        print "++++++++++++++++++",
        print response.selector.xpath(nxt_link_path),
        print "++++++++++++++++++"
        links = response.selector.xpath(prod_link_path).extract()
        print len(links)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_details_page)

    def parse_details_page(self, response):
        pass
        # print response.selector.xpath('//div[@id="product_tabs_description_tabbed_contents"]').extract()
    