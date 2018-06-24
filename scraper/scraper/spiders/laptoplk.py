# -*- coding: utf-8 -*-
import scrapy
import json


class LaptoplkSpider(scrapy.Spider):
    name = 'laptoplk'
    allowed_domains = ['laptop.lk']
    start_urls = ['http://laptop.lk/']

    def parse(self, response):
        links =  response.selector.xpath('//ul[@id="menu"]/li/div//a[@class="link7"]/@href').extract()
        for link in links:
            full_url = self.start_urls[0] + "/" + link
            yield scrapy.Request(full_url, callback=self.parse_details_page)

    def parse_details_page(self, response):
        currPageData = {}
        page = response.url.split("/")[-1]
        filename = 'data/processed/laptoplk/%s.json' % page
        url = self.start_urls[0]+page
        currPageData["url"] = url
        currPageData["title"] = response.xpath('//div[@class="Pro"]/h2/text()').extract()[0]
        currPageData["data"] = response.xpath('//div[@class="Pro"]').extract()[0]


        with open(filename, 'w') as fp:
            json.dump(currPageData, fp)
        # with open(filename, 'wb') as f:
        #     details = response.xpath('//div[@class="Pro"]').extract()
        #     print details
        #     f.write(str(details))
        self.log('Saved file %s' % filename)


