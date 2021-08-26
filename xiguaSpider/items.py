# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiguaspiderItem(scrapy.Item):
    detailUrl = scrapy.Field()
    title = scrapy.Field()
    dianzanCount = scrapy.Field()
    shoucangCount = scrapy.Field()
    fenxiangCount = scrapy.Field()
    viewCount = scrapy.Field()
    publishTime = scrapy.Field()
    publishAuthor = scrapy.Field()
    fensiCount = scrapy.Field()
    videoCount = scrapy.Field()
    videoUrl = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()
    commentCount = scrapy.Field()
    comments = scrapy.Field()
    Authorid = scrapy.Field()


