import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from crawler.items import crawlerItem, DynamicItem
import urllib.parse as urlparse
from collections import OrderedDict
import datetime

class MySpider(CrawlSpider):
  name = "spider"
  allowed_domains = ["ardmediathek.de"]
  start_urls = ["https://www.ardmediathek.de/ard"]
  rules = (
  Rule(LinkExtractor(allow=('/ard/video')), follow=True, callback='parse_link'),
  Rule(LinkExtractor(allow=('/ard/sendung')), follow=True, callback='parse_link'),
  Rule(LinkExtractor(allow=('/ard',)),follow=True)
  )

  def parse_link(self,response):
      page = Selector(response)
      item = OrderedDict()
      item["Request_time"] = str(datetime.datetime.now())
      item["Request_url"] = response.request.url
      #item["site_content"] = response.body

      item["Title"] = page.xpath("//h2[@class='H2-sc-1h18a06-3 khdvFh']/text()").get()
      item["Details"] = page.css('span[class="H4-sc-1h18a06-5 eROOGJ"] ::text').get()
      item["Beschreibung"] = page.css('p[class="P-sc-1ec4vuh-0 fcwbOf"] ::text').get()
      item["Verfügbar_bis"] = page.css('div[class="Available-pae2yt-6 jexgYU"] ::text').getall()
      item["Bild"] = page.css('div[class="PictureCredit-pae2yt-8 cJdkZe"] ::text').getall()

      return DynamicItem( **item )
