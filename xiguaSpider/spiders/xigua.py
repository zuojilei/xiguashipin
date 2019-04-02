# -*- coding: utf-8 -*-
import scrapy
import json
import xlwt
import datetime

from ..items import XiguaspiderItem

# https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_xg_movie&utm_source=toutiao&widen=1&tadrequire=true&as=A1356CB8354CB7B&cp=5C85ECBB27BB0E1&_signature=ojnZNhAa.ssIFpm2yASWDqI52S
# https://www.ixigua.com/api/pc/feed/?max_behot_time=1552274468&category=subv_xg_movie&utm_source=toutiao&widen=1&tadrequire=true&as=A1157C68A5DD8CE&cp=5C85EDA82C2E5E1&_signature=ojnZNhAa.ssIFpm2yAQSOKI52S

"""
西瓜视频：xigua
"""

class XiguaSpider(scrapy.Spider):
    name = 'xigua'
    allowed_domains = ['ixigua.com']
    start_urls = ['https://www.ixigua.com/api/pc/feed/?min_behot_time=0&category=subv_xg_movie&utm_source=toutiao&widen=1&tadrequire=true&as=A1153CD8459DA0F&cp=5C85ED8AE0BF1E1&_signature=ojnZNhAa.ssIFpm2yASWDqI52S']
    doc_url = 'https://www.ixigua.com/api/pc/feed/?max_behot_time={}&category=subv_xg_movie&utm_source=toutiao&widen=1&tadrequire=true&as=A185AC288847AA0&cp=5C88172A3A40AE1&_signature=YaQQuxAbPTDLi1A75tbnUmGkEK'
    base_url = 'https://www.ixigua.com'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'xiguaSpider.middlewares.SeleniumXigua': 10
        },
        'ITEM_PIPELINES':{
           'xiguaSpider.pipelines.XiguaspiderPipeline': 20,
        },
        # 'DOWNLOAD_DELAY': 10
    }

    def parse(self, response):
        """
        驱动浏览器请求初始url拿到max_behot_time
        :param response:
        :return:
        """
        html = response.text
        data = self.replace(html)
        max_behot_time = json.loads(data)['data'][0]['behot_time']
        url = self.doc_url.format(max_behot_time)
        yield scrapy.Request(url=url,callback=self.get_info,dont_filter=True)

    def get_info(self,response):
        """
        拿取列表页信息，同时生成详情页和下一页请求的url
        :param response:
        :return:
        """
        try:
            html = response.text
            data = self.replace(html)
            contents = json.loads(data)['data']
            for content in contents:
                title = content['title']
                source = content['source']
                video_duration_str = content.get('video_duration_str',0)
                comments_count = content.get('comments_count',0)
                video_play_count = content.get('video_play_count',0)
                source_url = content['source_url']
                meta = {
                    'title':title,
                    'source':source,
                    'video_duration_str':video_duration_str,
                    'comments_count':comments_count,
                    'video_play_count':video_play_count
                }
                yield scrapy.Request(url = self.base_url + source_url,meta=meta,callback=self.get_detail,dont_filter=True)

            #生成下一页请求
            max_behot_time = json.loads(data)['next']['max_behot_time']
            url = self.doc_url.format(max_behot_time)
            yield scrapy.Request(url=url, callback=self.get_info, dont_filter=True)

        except Exception as e:
            print(e)

    def get_detail(self,response):
        """
        请求详情页，拿取信息
        :param response:
        :return:
        """
        try:
            item = XiguaspiderItem()
            title = response.meta['title']
            source = response.meta['source']
            video_duration_str = response.meta['video_duration_str']
            comments_count = response.meta['comments_count']
            video_play_count = response.meta['video_play_count']
            url = response.url
            digg = response.xpath('//span[@class="digg"]/text()').extract_first()
            bury = response.xpath('//span[@class="bury"]/text()').extract_first()
            time_info = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

            item['title'] = title
            item['source'] = source
            item['video_duration_str'] = video_duration_str
            item['comments_count'] = comments_count
            item['video_play_count'] = video_play_count
            item['url'] = url
            item['digg'] = (digg if digg else 0)
            item['bury'] = (bury if bury else 0)
            item['time_info'] = time_info
            yield item
        except Exception as e:
            print(e)

    def replace(self,html):
        """去除标签生成json字符串"""
        html = html.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
        html = html.replace('<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
        html = html.replace('</pre></body></html>', '')
        return html



