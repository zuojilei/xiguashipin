from scrapy import cmdline
import sys
import os


def run_spider(spider_name):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    cmd_list = ['scrapy', 'crawl']
    cmd_list.append(spider_name)
    cmdline.execute(cmd_list)


if __name__ == '__main__':
    run_spider(spider_name='xigua')