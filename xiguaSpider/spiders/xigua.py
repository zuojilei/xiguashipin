# -*- coding: utf-8 -*-
import re
import time

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
            yield scrapy.Request(url=detailUrl, callback=self.get_detail, dont_filter=True)

    def get_detail(self, response):
        # with open('list.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        item = XiguaspiderItem()

        # 详情页地址
        item['detailUrl'] = response.url

        # 标题
        try:
            title = response.xpath('//div[@class="videoTitle"]/h1/text()').get()
            item['title'] = title.strip()
        except Exception:
            item['title'] = ""
            print("标题获取error!!!")

        # 点赞数
        try:
            dianzan = response.xpath('//div[@class="video_action"]/button[1]/@aria-label').get()
            dianzanCountRe = re.search(r'\d+', dianzan, re.DOTALL)
            item['dianzanCount'] = int(dianzanCountRe.group()) if dianzanCountRe else 0
        except Exception:
            item['dianzanCount'] = 0
            print("点赞数获取error!!!")

        # 收藏数
        try:
            shoucang = response.xpath('//div[@class="video_action"]/button[2]/@aria-label').get()
            shoucangRe = re.search(r'\d+', shoucang, re.DOTALL)
            item['shoucangCount'] = int(shoucangRe.group()) if shoucangRe else 0
        except Exception:
            item['shoucangCount'] = 0
            print("收藏数获取error!!!")

        # 分享数
        try:
            fenxiangCount = response.xpath('//div[@class="video_action"]/button[3]/@aria-label').get()
            item['fenxiangCount'] = int(fenxiangCount) if fenxiangCount else 0
        except Exception:
            item['fenxiangCount'] = 0
            print("分享数获取error!!!")

        # 观看次数
        try:
            viewCount = response.xpath('//p[@class="videoDesc__videoStatics"]/span[1]/text()').get()
            item['viewCount'] = viewCount.split('次观看')[0]
        except Exception:
            item['viewCount'] = 0
            print("观看次数获取error!!!")

        # 发布时间
        try:
            publishTimeTamp = response.xpath(
                '//span[@class="videoDesc__publishTime xiguabuddy"]/@data-publish-time').get()
            publishTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(publishTimeTamp)))
            item['publishTime'] = publishTime
        except Exception:
            item['publishTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("发布时间获取error!!!")

        # 发布作者
        try:
            publishAuthor = response.xpath('//span[@class="user__name isVip"]/text()').get()
            item['publishAuthor'] = publishAuthor.strip()
        except Exception:
            item['publishAuthor'] = ""
            print("发布作者获取error!!!")

        # 粉丝数
        try:
            fensiCount = response.xpath('//a[@class="author_statics"]/span[1]/text()').get()
            item['fensiCount'] = fensiCount.strip()
        except Exception:
            item['fensiCount'] = 0
            print("粉丝数获取error!!!")

        # 视频总数
        try:
            videoCount = response.xpath('//a[@class="author_statics"]/span[3]/text()').get()
            item['videoCount'] = videoCount if videoCount else 0
        except Exception:
            item['videoCount'] = 0
            print("视频总数获取error!!!")

        dataJsonRe = re.search(r'<script data-react-helmet="true" type="application/ld\+json">(.*?)</script>',
                               response.text, re.DOTALL)
        if dataJsonRe:
            datajson = dataJsonRe.group(1)
            data = json.loads(datajson)

            # 简介
            item['description'] = data['description'].strip()

            # 视频地址
            item['videoUrl'] = data['embedUrl']

            # 封面图片
            item['images'] = data['thumbnailUrl'][0]
        yield item
