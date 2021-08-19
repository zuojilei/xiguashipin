# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiguaspiderItem(scrapy.Item):
    title = scrapy.Field()
    dianzan = scrapy.Field()
    shoucang = scrapy.Field()
    fenxiang = scrapy.Field()
    viewCount = scrapy.Field()
    publishTime = scrapy.Field()
    publishAuthor = scrapy.Field()
    fensiCount = scrapy.Field()
    videoCount = scrapy.Field()
    url = scrapy.Field()
