# -*- coding: utf-8 -*-
import scrapy


class SoftlogicSpider(scrapy.Spider):
    name = 'softlogic'
    allowed_domains = ['mysoftlogic.lk']
    start_urls = ['https://mysoftlogic.lk/search?department=2&category=6']
    base_url = 'https://mysoftlogic.lk'

    def parse(self, response):
        links =  response.selector.xpath('//div[@class="product-item"]//a/@href').extract()
        print len(links)
        for link in links:
            full_url = self.start_urls[0] + "/" + link
            yield scrapy.Request(full_url, callback=self.parse_details_page)

    def parse_details_page(self, response):
        page = response.url.split("/")[-1]
        filename = 'data/softlogic/softlogic-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
