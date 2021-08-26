# -*- coding: utf-8 -*-
import re
import time

import scrapy
import json

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
        'DOWNLOAD_DELAY': 5
    }

    def parse(self, response):
        """
        驱动浏览器请求初始url拿到max_behot_time
        :param response:
        :return:
        """
        hrefs = response.xpath('//a[@class="HorizontalFeedCard__title color-link-content-primary"]/@href').getall()
        for href in hrefs:
            try:
                detailUrl = "https://www.ixigua.com{}".format(href)
                yield scrapy.Request(url=detailUrl, callback=self.get_detail, dont_filter=True)
            except Exception as e:
                print(e)

    def get_detail(self, response):
        # with open('list.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        item = XiguaspiderItem()

        # 详情页地址
        item['detailUrl'] = response.url

        # 发布人id
        item['Authorid'] = ""  # 没有获取

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

        # 评论数
        try:
            commentCount = response.xpath('//div[@class="commentCount"]').get()
            commentCountRe = re.search(r'\d+', commentCount, re.DOTALL)
            item['commentCount'] = int(commentCountRe.group()) if commentCountRe else 0
        except Exception:
            item['commentCount'] = 0
            print("评论数获取error!!!")

        item["comments"] = self.get_comment(response)

        dataJsonRe = re.search(r'<script data-react-helmet="true" type="application/ld\+json">(.*?)</script>',
                               response.text, re.DOTALL)
        if dataJsonRe:
            datajson = dataJsonRe.group(1)
            data = json.loads(datajson)

            # 简介
            item['description'] = data['description'].strip()

            # 视频地址
            item['videoUrl'] = data['embedUrl']

        print(item)
        yield item

    @staticmethod
    def get_comment(response):
        """获取评论"""

        commentList = []
        elems = response.xpath('//div[@class="commentList"]/div[@class="commentItem"]')
        if elems:
            for elem in elems:

                # 评论人
                comment_name = elem.xpath('.//div[@class="commentItem__userName"]/span[@class="user__name"]/text()').get()
                commentUser = comment_name.strip() if comment_name else ""

                # 评论时间
                comment_time = elem.xpath('.//div[@class="commentItem__publishTime"]/text()').get()
                commentTime = comment_time.strip() if comment_time else ""

                # 评论内容
                comment_content = elem.xpath('.//div[@class="commentItem__text"]//text()').get()
                commentDetail = comment_content.strip() if comment_content else ""
                commentList.append({"commentUser": commentUser,
                                    "commentTime": commentTime,
                                    "commentDetail": commentDetail})

        return commentList

