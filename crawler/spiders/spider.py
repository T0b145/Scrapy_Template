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
  allowed_domains = ["mobile.de"]
  start_urls = ["https://suchen.mobile.de/fahrzeuge/search.html?c=VanMotorhome&con=USED&isSearchRequest=true&ml=%3A200000&p=%3A30000&s=Motorhome&sfmr=false&vc=Motorhome"]
  rules = (
  Rule(LinkExtractor(allow=('fahrzeuge/details.html'), restrict_xpaths=["//div[contains(@class,'cBox--resultList')]"]), follow=False, callback="parse_link"),
  Rule(LinkExtractor(tags=("span"),attrs=('data-href'), restrict_xpaths=["//ul[@class='pagination']"]), follow=True)
  )

  def parse_link(self,response):
      page = Selector(response)
      item = OrderedDict()
      item["Request_time"] = str(datetime.datetime.now())
      item["Request_url"] = response.request.url
      #item["site_content"] = response.body

      item["Title"] = page.xpath("//h1[@id='rbt-ad-title']//text()").get()
      item["Preis"] = page.xpath("//div[@id='rbt-pt-v']//text()").get()
      item["Kategorie"] = page.xpath("//div[@id='rbt-category-v']//text()").get()
      item["Fahrzeugnummer"] = page.xpath("//div[@id='rbt-sku-v']//text()").get()
      item["Kilometerstand"] = page.xpath("//div[@id='rbt-mileage-v']//text()").get()
      item["Leistung"] = page.xpath("//div[@id='rbt-power-v']//text()").get()
      item["Kraftstoffart"] = page.xpath("//div[@id='rbt-fuel-v']//text()").get()
      item["Getriebe"] = page.xpath("//div[@id='rbt-transmission-v']//text()").get()
      item["Schadstoffklasse"] = page.xpath("//div[@id='rbt-emissionClass-v']//text()").get()
      item["Umweltplakette"] = page.xpath("//div[@id='rbt-emissionsSticker-v']//text()").get()
      item["Erstzulassung"] = page.xpath("//div[@id='rbt-firstRegistration-v']//text()").get()
      item["Anzahl der Fahrzeughalter"] = page.xpath("//div[@id='rbt-numberOfPreviousOwners-v']//text()").get()
      item["Zulässiges Gesamtgewicht"] = page.xpath("//div[@id='rbt-licensedWeight-v']//text()").get()
      item["HU"] = page.xpath("//div[@id='rbt-hu-v']//text()").get()
      item["Klimatisierung"] = page.xpath("//div[@id='rbt-climatisation-v']//text()").get()
      item["Einparkhilfe"] = page.xpath("//div[@id='rbt-parkAssists-v']//text()").get()
      item["Farbe"] = page.xpath("//div[@id='rbt-color-v']//text()").get()
      item["Länge"] = page.xpath("//div[@id='rbt-vehicleLength-v']//text()").get()
      item["Breite"] = page.xpath("//div[@id='rbt-vehicleWidth-v']//text()").get()
      item["Höhe"] = page.xpath("//div[@id='rbt-vehicleHeight-v']//text()").get()
      item["Ausstattung"] = page.xpath("//div[@id='rbt-features']//div[@class='bullet-list']//text()").getall()
      item["Besondere Merkmale"] = page.xpath("//li[@class='vip-vehicle-highlights__item']//text()").getall()
      item["Fahrzeugbeschreibung"] = page.xpath("//div[@class='g-col-12 description']//li//text()").getall()
      item["Special Services"] = page.xpath("//div[@class='g-col-12 special-services']//span//text()").getall()
      item["Händler"] = page.xpath("//p[@id='rbt-db-address']//text()").getall()

      return DynamicItem( **item )
