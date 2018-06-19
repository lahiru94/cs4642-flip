# -*- coding: utf-8 -*-
import scrapy


class LaptoplkSpider(scrapy.Spider):
    name = 'laptoplk'
    allowed_domains = ['laptop.lk']
    start_urls = ['http://laptop.lk/']

    def parse(self, response):
        links =  response.selector.xpath('//ul[@id="menu"]/li/div//a[@class="link7"]/@href').extract()
        print len(links)
        for link in links:
            full_url = self.start_urls[0] + "/" + link
            yield scrapy.Request(full_url, callback=self.parse_details_page)

    def parse_details_page(self, response):
        page = response.url.split("=")[-1]
        filename = 'data/laptoplk/laplk-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


