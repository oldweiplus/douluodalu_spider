# -*- coding: utf-8 -*-
import scrapy

from douluodalu.items import DouluodaluItem


class DownloadfileSpiderSpider(scrapy.Spider):
    name = 'downloadfile_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/2244426/?from=showing']

    # 测试下载
    def parse(self, response):
        url = response.xpath("/html[@class='ua-windows ua-webkit']/body/div[@id='wrapper']/div[@id='content']/div[@class='grid-16-8 clearfix']/div[@class='article']/div[@class='indent clearfix']/div[@class='subjectwrap clearfix']/div[@class='subject clearfix']/div[@id='mainpic']/a[@class='nbgnbg']/img/@src").extract_first()
        item = DouluodaluItem()
        item["img_url"] = [url]
        item["title"] = "斗罗大陆"
        yield item
