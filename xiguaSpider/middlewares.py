# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .settings import PATH
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import re


class SeleniumXigua(object):
    """驱动浏览器访问**详情页"""
    options = Options()
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument("service_args = ['–ignore - ssl - errors = true', '–ssl - protocol = TLSv1']")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('disable-infobars')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"')

    def process_request(self, request, spider):
        print(request.url)
        driver = webdriver.Chrome(
            options=self.options,
            executable_path=PATH)
        driver.maximize_window()
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.get(request.url)
        time.sleep(5)
        # 判断当前url是否为详情url，是，控制滚轮下滑
        if re.search(r'\d+', request.url, re.DOTALL):
            self.drop_down(driver)
        response = HtmlResponse(url=driver.current_url, request=request,
                                body=driver.page_source, encoding='utf-8')
        driver.close()
        return response

    def drop_down(self, driver):
        '''
        页面下拉尽量模拟成人下拉
        :return:
        '''
        for x in range(1, 10, 3):  # 1 3 5 7...19
            try:
                time.sleep(5)
                j = x / 10  # 分数 1/9 3/9 5/9 7/9...
                # js下拉页面
                js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
                driver.execute_script(js)
            except:
                break


class XiguaspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XiguaspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
