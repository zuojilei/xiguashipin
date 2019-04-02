# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiguaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    video_duration_str = scrapy.Field()
    comments_count = scrapy.Field()
    video_play_count = scrapy.Field()
    url = scrapy.Field()
    digg = scrapy.Field()
    bury =scrapy.Field()
    time_info = scrapy.Field()
