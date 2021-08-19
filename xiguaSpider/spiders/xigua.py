# -*- coding: utf-8 -*-
import re

import scrapy
import json
import xlwt
import datetime

from ..items import XiguaspiderItem


"""
西瓜视频：xigua
"""


class XiguaSpider(scrapy.Spider):
    name = 'xigua'
    allowed_domains = ['ixigua.com']
    start_urls = ["https://www.ixigua.com/channel/yingshi/"]
    base_url = 'https://www.ixigua.com'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'xiguaSpider.middlewares.SeleniumXigua': 10
        },
        'ITEM_PIPELINES': {
            # 'xiguaSpider.pipelines.XiguaspiderPipeline': 20,
        },
        'DOWNLOAD_DELAY': 3
    }

    def parse(self, response):
        """
        驱动浏览器请求初始url拿到max_behot_time
        :param response:
        :return:
        """
        hrefs = response.xpath('//a[@class="HorizontalFeedCard__title color-link-content-primary"]/@href').getall()
        for href in hrefs:
            detailUrl = "https://www.ixigua.com{}".format(href)
            print(detailUrl)
            yield scrapy.Request(url=detailUrl, callback=self.get_detail, dont_filter=True)
            break

    def get_detail(self, response):
        try:
            item = XiguaspiderItem()
            title = response.xpath('//div[@class="videoTitle"]/h1/text()').get()
            dianzan = response.xpath('//div[@class="video_action"]/button[1]/@aria-label').get()
            shoucang = response.xpath('//div[@class="video_action"]/button[2]/@aria-label').get()
            fenxiang = response.xpath('//div[@class="video_action"]/button[3]/@aria-label').get()
            viewCount = response.xpath('//p[@class="videoDesc__videoStatics"]/span[1]/text()').get()
            publishTime = response.xpath('//p[@class="videoDesc__videoStatics"]/span[3]/@data-publish-time').get()
            publishAuthor = response.xpath('//span[@class="user__name isVip"]/text()').get()
            fensiCount = response.xpath('//a[@class="author_statics"]/span[1]/text()').get()
            videoCount = response.xpath(';//a[@class="author_statics"]/span[3]/text()').get()
            url = response.url
            item['title'] = title.strip()
            item['dianzan'] = dianzan
            item['shoucang'] = shoucang
            item['fenxiang'] = fenxiang
            item['viewCount'] = viewCount
            item['publishTime'] = publishTime
            item['publishAuthor'] = publishAuthor
            item['fensiCount'] = fensiCount
            item['videoCount'] = videoCount
            item['url'] = url
            print(item)
            yield item
        except Exception as e:
            print(e)
