# -*- coding: utf-8 -*-
import scrapy
import re
from douluodalu.items import DouluodaluItem
from scrapy_splash.request import SplashRequest


class DouluoSpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'douluo_spider'
    # 允许的域名
    allowed_domains = ['www.manhuatai.com']
    # 入口url，扔到调度器
    start_urls = ['https://www.manhuatai.com/douluodalu']

    # 默认的解析方法
    def parse(self, response):
        num_list = response.xpath(
            "/html/body/div[@class='wrapper']/div[@class='mainctx']/div[@class='block1 clearfix']/div[@class='l']/div[@class='mhjs clearfix']/div[@id='alllist']/div[@class='mt10']/div[@class='mhlistbody']/ul[@id='topic1']/li")
        for index, i_item in enumerate(num_list):
            geturl = "https://www.manhuatai.com" + i_item.xpath("./a/@href").extract_first()
            lua = """
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
                    splash:go("{urladdr}")
                    splash:wait(0.5)
                    return {htmltype}
                    """.format(urladdr=geturl, htmltype="{html = splash:html()}")
            splash_args = {"lua_source": lua}
            yield SplashRequest(geturl, endpoint='run', args=splash_args, callback=self.getpath)
        # yield douluo_item

    def getpath(self, response):
        douluo_item = DouluodaluItem()
        douluo_item["title"] = response.xpath(
            "/html/body/div[@class='mh_wrap tc'][1]/div[@class='mh_readtitle']/h1/strong/text()").extract_first()
        # 获取没章节的图片总数
        countstr = response.xpath(
            "/html/body/div[@id='comiclist']/div[@class='mh_comicpic']/text()").extract_first().replace(' ', '')[-3:]
        countpages = re.findall("\d+", countstr)[0]
        douluo_item["countpic"] = countpages
        pic_first = response.xpath("/html/body/div[@id='comiclist']/div[@class='mh_comicpic']/img/@src").extract_first()
        img_urls = {}
        for i in range(1, int(countpages) + 1):
            img_url = pic_first.replace("1.jpg-mht.middle.webp", str(i) + ".jpg-mht.middle.webp")
            img_urls[i] = img_url
        douluo_item["img_urls"] = img_urls
        yield douluo_item
