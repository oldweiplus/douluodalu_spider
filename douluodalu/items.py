# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouluodaluItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 章节名称
    title = scrapy.Field()
    # 章节图片数
    countpic = scrapy.Field()
    # 下载图片的地址
    img_urls = scrapy.Field()
    # 下载图片的名字
    img_name = scrapy.Field()


