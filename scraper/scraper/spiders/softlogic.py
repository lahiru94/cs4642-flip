# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class SoftlogicSpider(scrapy.Spider):
    name = 'softlogic'
    allowed_domains = ['mysoftlogic.lk']
    start_urls = ['https://mysoftlogic.lk/search?department=2&category=6']
    base_url = 'https://mysoftlogic.lk'

    def parse(self, response):
        links =  response.selector.xpath('//div[@class="product-item"]/figure/figcaption/a/@href').extract()
        print len(links)
        for link in links:
            product_id = link.split("=")[-1]
            print product_id
            url = 'https://mysoftlogic.lk/product-page/get-product-details'
            form_data = {"product_id":product_id}
            yield scrapy.FormRequest(url, callback=self.parse_details, method='POST', headers={"X-Requested-With":"XMLHttpRequest"}, formdata=form_data)

    def parse_details_page(self, response):
        page = response.url.split("/")[-1]
        filename = 'data/softlogic/softlogic-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse_details(self, response):
        print response.body
