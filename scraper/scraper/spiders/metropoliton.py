# -*- coding: utf-8 -*-
import scrapy
import json
import utils


class MetropolitonSpider(scrapy.Spider):
    name = 'metropoliton'
    allowed_domains = ['mcentre.lk']
    start_urls = ['http://mcentre.lk/']

    def parse(self, response):
        link_path = '//div[@class="no_blink_cls"]/div[not(@class="menu4")andnot(@class="menu42")and@class="menu parrent-arrow"]//a/@href'
        links =  response.selector.xpath(link_path).extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_products_page)
            

    def parse_products_page(self, response):
        prod_link_path = '//h2[@class="product-name"]/a/@href'
        nxt_link_path = '//a[@title="Next"]/@href'
        nxt_links = response.selector.xpath(nxt_link_path).extract()

        if(len(nxt_links)>0):
            yield scrapy.Request(nxt_links[0], callback=self.parse_products_page)

        links = response.selector.xpath(prod_link_path).extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_details_page)

    def parse_details_page(self, response):

        url =  response.url
        title = response.selector.xpath('//div[@class="product-name"]/h1/text()').extract_first()
        summary = response.selector.xpath('//div[@class="short-description"]').extract_first()
        specs = response.selector.xpath('//div[@id="product_tabs_description_tabbed_contents"]').extract_first()
        price = response.selector.xpath('//span[@class="price"]/text()').extract_first()
        model_id = response.selector.xpath('/html/head/meta[@name="keywords"]/@content').extract_first()
        
        if(price is None):
            price = response.selector.xpath('//span[@class="special-price"]/text()').extract_first()

        url_components = url.split("/")
        page = url_components[-1][:-5]
        filename = 'data/processed/metropoliton/%s.json' % page
        catogory = url_components[-2]
        brand = url_components[-1].split("-")[0]

        specs = utils.extract_text(specs)
        summary = utils.extract_text(summary)

        currPageData = {}        
        currPageData["url"] = url
        currPageData["title"] = title
        currPageData["summary"] = summary

        currPageData["catogory"] = catogory
        currPageData["brand"] = brand
        currPageData["model_id"] = model_id
        currPageData["specs"] = specs
        currPageData["price"] = price

        with open(filename, 'w') as fp:
            json.dump(currPageData, fp)


    
    