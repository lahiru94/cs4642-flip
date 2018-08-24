# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import json
import utils

class SoftlogicSpider(scrapy.Spider):
    name = 'softlogic'
    allowed_domains = ['mysoftlogic.lk']
    start_urls = ['https://mysoftlogic.lk/search?department=2&category=6']
    base_url = 'https://mysoftlogic.lk'

    # def parse(self, response):
    #     links =  response.selector.xpath('//div[@class="product-item"]/figure/figcaption/a/@href').extract()
    #     for link in links:
    #         product_id = link.split("=")[-1]
    #         url = 'https://mysoftlogic.lk/product-page/get-product-details'
    #         form_data = {"product_id":product_id}
    #         yield scrapy.FormRequest(url, callback=self.parse_details, method='POST', headers={"X-Requested-With":"XMLHttpRequest"}, formdata=form_data)

    def parse(self, response):
        links =  response.selector.xpath('//div[@class="product-item"]/figure/figcaption/a/@href').extract()
        for link in links:
            full_link = self.base_url + link
            yield scrapy.Request(full_link,callback=self.parse_details_page)

    def parse_details_page(self, response):
        
        url = response.url
        title = response.selector.xpath('//title/text()').extract_first().strip()
        summary = response.selector.xpath('meta[@itemprop="description"]/@content').extract_first()

        catogory = response.selector.xpath('//ol/li[position()=4]/a/text()').extract_first()
        brand = response.selector.xpath('//ol/li[position()=5]/a/text()').extract_first()

        curr_page_data = {}        
        curr_page_data["url"] = url
        curr_page_data["title"] = title
        curr_page_data["summary"] = summary

        curr_page_data["catogory"] = catogory
        curr_page_data["brand"] = brand
        curr_page_data["model_id"] = ""
        curr_page_data["specs"] = ""
        curr_page_data["price"] = ""


        product_id = response.url.split('/')[-1]
        ajax_call_url = 'https://mysoftlogic.lk/product-page/get-product-details'
        form_data = {"product_id":product_id}

        ajax_req = scrapy.FormRequest(ajax_call_url, callback=self.get_specs, method='POST', headers={"X-Requested-With":"XMLHttpRequest"}, formdata=form_data)
        ajax_req.meta['page_data'] = curr_page_data
        ajax_req.meta['id'] = url.split("/")[-1]
        yield ajax_req

    def get_specs(self, response):

        item_code = response.meta['id']
        page_data =  response.meta['page_data']

        data = json.loads(response.text)
        specs = data["specifications"]
        specs = utils.extract_text(specs)
        page_data["specs"] =  specs 

        price_url = "https://mysoftlogic.lk/product-page/variation-detail/" + item_code

        ajax_req = scrapy.Request(price_url, callback=self.get_price, headers={"X-Requested-With":"XMLHttpRequest"})
        ajax_req.meta['page_data'] = page_data
        yield ajax_req


    def get_price(self, response):

        page_data = response.meta['page_data']
        data =  json.loads(response.text)
        page_data['price'] = data['price']
        page_data['model_id'] = data['erp']
        page_data["vendor"] = "softlogic"


        yield page_data




