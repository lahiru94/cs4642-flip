# -*- coding: utf-8 -*-
import scrapy
import json
import utils

class BarclaysSpider(scrapy.Spider):
    name = 'barclays'
    allowed_domains = ['barclays.lk']
    start_urls = ['http://www.barclays.lk/bc/AtoZdisplay.asp?Type=01&TpData=']
    base_url = 'http://www.barclays.lk/bc'
    links = {}

    def parse(self, response):
        links =  response.selector.xpath('//li/a/@href').extract()
        print len(links)
        for link in links:
            full_url = self.base_url + "/" + link
            yield scrapy.Request(full_url, callback=self.parse_products_page)

    def parse_products_page(self, response):
        links =  response.selector.xpath('//div[@class="product-thumbnail"]/div/a/@href').extract()
        for link in links:
            full_url =  link
            yield scrapy.Request(full_url, callback=self.parse_details_page)
    
    def parse_details_page(self, response):
        
        page = response.url.split("/")[-1]
        filename = 'data/processed/barclays/%s.json' % page

        url = response.url
        title = response.selector.xpath('//title/text()').extract_first()
        summary = response.selector.xpath('//div[@class="product-view-area"]//form/ul').extract_first()
        summary = utils.extract_text(summary)

        catogory = response.selector.xpath('//div[@class="product-view-area"]//form/ul/li[contains(text(),"Categories")]/a/text()').extract_first()
        brand = response.selector.xpath('//div[@class="product-view-area"]//form/ul/li[contains(text(),"Brands")]/a/text()').extract_first()
        model_id = response.selector.xpath('//div[@class="product-view-area"]//form/ul/li[contains(text(),"Model")]/text()').extract_first()
        model_id = utils.extract_text(model_id)
        specs = response.selector.xpath('//div[@id="description"]/div/p').extract_first()
        specs = utils.extract_text(specs)
        price = response.selector.xpath('//span[@class="price"]/text()').extract_first()
        price = utils.clean_price(price)

        curr_page_data = {}        
        curr_page_data["url"] = url
        curr_page_data["title"] = title
        curr_page_data["summary"] = summary

        curr_page_data["catogory"] = catogory
        curr_page_data["brand"] = brand
        curr_page_data["model_id"] = model_id
        curr_page_data["specs"] = specs
        curr_page_data["price"] = price

        with open(filename, 'w') as fp:
            json.dump(curr_page_data, fp)

        