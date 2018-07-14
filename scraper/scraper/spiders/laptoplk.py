# -*- coding: utf-8 -*-
import scrapy
import json
import utils


class LaptoplkSpider(scrapy.Spider):
    name = 'laptoplk'
    allowed_domains = ['laptop.lk']
    start_urls = ['http://laptop.lk/']

    def parse(self, response):
        links =  response.selector.xpath('//ul[@id="menu"]/li/div//a[@class="btn-all"]/@href').extract()
        for link in links:
            full_url = self.start_urls[0] + "/" + link
            request = scrapy.Request(full_url, callback=self.parse_products_page)
            request.meta['test'] = "TEST"
            yield request

    def parse_products_page(self, response):
        print response.meta['test']
        catogory = response.selector.xpath('//h2[@id="pgeHdng"]/text()').extract_first()
        if(catogory is None):
            catogory = response.selector.xpath('//div[@class="All_laptop"]/h2/text()').extract_first()

        print catogory

    def parse_details_page(self, response):

        page = response.url.split("/")[-1]
        filename = 'data/processed/laptoplk/%s.json' % page

        url = response.url
        title = response.selector.xpath().extract_first()
        summary = response.selector.xpath().extract_first()
        summary = utils.extract_text(summary)

        catogory = response.selector.xpath().extract_first()
        model_id = response.selector.xpath('//li/b[contains(text(),"Model")]/following-sibling::strong/text()').extract_first()
        brand = model_id.split(" ")[0]
        specs = response.selector.xpath().extract_first()
        specs = utils.extract_text(specs)
        price = response.selector.xpath('//b[contains(text(),"LKR")]/text()').extract_first()
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
        # with open(filename, 'wb') as f:
        #     details = response.xpath('//div[@class="Pro"]').extract()
        #     print details
        #     f.write(str(details))
        self.log('Saved file %s' % filename)


