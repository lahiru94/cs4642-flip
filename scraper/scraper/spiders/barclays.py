# -*- coding: utf-8 -*-
import scrapy
import json

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
            full_url = self.base_url + "/" + link
            yield scrapy.Request(full_url, callback=self.parse_details_page)
    
    def parse_details_page(self, response):
        currUrl = response.url
        page = response.url.split("/")[-1]
        self.links[page] = currUrl
        filename = 'data/barclays/%s.html' % page

        with open(filename, 'wb') as f:
            f.write(response.body)
            # details = response.selector.xpath('//section[@class="main-container col1-layout"]').extract()
            # f.write(details)
        self.log('Saved file %s' % filename)

        with open('data/barclays/links.json', 'w') as fp:
            json.dump(self.links, fp)

        