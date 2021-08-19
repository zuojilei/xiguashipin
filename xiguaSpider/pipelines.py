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
        self.ws.append(['标题', '视频长度', '账号名', '链接', '播放量', '评论数', '点赞数', '不喜欢数', '数据手机时间'])

    def process_item(self, item, spider):
        line = [item['title'], item['video_duration_str'], item['source'], item['url'],
                item['video_play_count'], item['comments_count'], item['digg'],
                item['bury'], item['time_info']]
        self.ws.append(line)
        self.wb.save('西瓜视频.xlsx')

        return item
