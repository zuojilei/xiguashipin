# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook


class XiguaspiderPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['标题', '简介', '详情地址', '点赞数', '收藏数', '分享数', '观看次数', '发布时间', '发布作者', '粉丝数',
                        '视频总数', '视频地址', '封面图片'])

    def process_item(self, item, spider):
        line = [item['title'], item['description'], item['detailUrl'], item['dianzanCount'],
                item['shoucangCount'], item['fenxiangCount'], item['viewCount'], item['publishTime'],
                item['publishAuthor'], item['fensiCount']], item['videoCount'], item['videoUrl'], item['images']
        self.ws.append(line)
        self.wb.save('西瓜视频.xlsx')

        return item
