from scrapy.spiders import Spider

from scrapy.selector import Selector
import scrapy
from scrapy import signals
from urllib import parse
from scrapy.http import Request
from allwhitestreet.items import AllwhitestreetItem
import re
from datetime import date, datetime, timedelta
from selenium import webdriver
import time
today = date.today()
from lxml import etree
#strtoday = today.strftime('%Y-%m-%d')
import logging
logger = logging.getLogger('wwwww')
#class LogSpider(scrapy.Spider):
class DmozSpider(Spider):
    name = "whitestreet"
    allowed_domains = ["https://wallstreetcn.com"]
    start_urls = {
        "https://wallstreetcn.com/news/global?from=home"
    }


    def parse(self, response):
        #self.logger.info('Parse function called on %s', response.url)
        driver = webdriver.Firefox()
        driver.get(response.url)
        for i in range(3):
            driver.execute_script("window.scrollBy(0," + str(i * 1000 + 2000) + ")")
            time.sleep(3)
            if i == 2:
                #data = driver.page_source
                body = driver.page_source
                time.sleep(3)
                print("访问" + response.url)
                doc = etree.HTML(body)
                movies = doc.xpath('//div[@class="news-item__main"]/a/@href')
                time.sleep(2)
                for hua_urlss in movies:
                    #name = each_movie.xpath('a/text()').extract()
                    hua_url=str(hua_urlss)
                    print(hua_url)
                    #log.msg(hua_url)
                    self.logger.info(hua_url)
                    yield Request(url=parse.urljoin(response.url, hua_url),callback=self.parse_detail, dont_filter=True)
    def parse_detail(self, response):
        try:
            num = response.xpath('//span[@class="comment-item__text"]/text()').extract()[0]
        except:
            num =''
        if num =='':
            pass
        if len(num) != 4 and num !='':
            nums= int(re.sub("\D", "", num))
        else:
            nums =0
        try:
            times = response.xpath('//span[@class="meta-item__text"]/text()').extract()[0] or response.xpath('//span[@class="meta-item__text"]/text()').extract()[0]
            title = response.xpath('//div[@class="article__heading__title"]/text()').extract()[0] or response.xpath('//div[@class="article__heading__title"]/text()').extract()[0]
            uid = response.xpath("//a[@class= 'user-card__row__name']/@href").extract()[0]
            author = response.xpath("//a[@class= 'user-card__row__name']/text()").extract()[0]
            allwenzhang = response.xpath("//div[@class='user-card__row']/div[1]/div[@class='user-card-meta__value']/text()").extract()[0]
            fensi= response.xpath("//div[@class='user-card__row']/div[2]/div[@class='user-card-meta__value']/text()").extract()[0]
        except:
            times =''
            title =''
            uid = ''
            author =''
            allwenzhang=''
            fensi = ''
        if title=='' or uid =='' or author=='' or allwenzhang=='' or fensi=='' or times=='':
            pass
        today = date.today()

        print(title,times,uid)
        item = AllwhitestreetItem()
        item["url"] = response.url
        item['title'] = title
        item['nums'] = nums
        item['times']=times
        item['uid']=uid
        item['author']=author
        item['allwenzhang']=allwenzhang
        item['fensi']=fensi
        print(item['nums'])
        yield item