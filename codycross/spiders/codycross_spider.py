# -*- coding: utf-8 -*-
import scrapy
from ..items import CodycrossItem
from scrapy import Request
from urllib.parse import urljoin


class CodycrossScraper(scrapy.Spider):
	name = "spider"
	start_urls = ['https://codycross.info/tr']

	def parse(self, response):
		"""Bütün Kategorilerin linkini al"""
		for href in response.xpath("//div[@class='widget']/h2[@class='world']/a/@href"): 
			url=response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_kategori, encoding=response.encoding)

	def parse_kategori(self, response):
		"""Bütün Bulmacaların linklerini al"""
		bulmaca_link=response.xpath("//ul[@class='widget-games']/li[@class='packs']/a/@href")
		for i in bulmaca_link:
			link_bulmaca=response.urljoin(i.extract())
			yield scrapy.Request(link_bulmaca, callback=self.parse_bulmaca, encoding=response.encoding)

	def parse_bulmaca(self, response):
		"""Bütün soruların linklerini al"""
		soru_link=response.xpath("//div[@class='words']/p/a/@href")
		for j in soru_link:
			link_soru=response.urljoin(j.extract())
			yield scrapy.Request(link_soru, callback=self.parse_soru, encoding=response.encoding)

	def parse_soru(self, response):
		"""Bütün soruları ve cevapları al"""
		item=CodycrossItem()
		sorular=response.xpath("//html/body/div[2]/div[1]")
		for k in sorular:
			questions=response.xpath("//div[4]/text()").extract()
			item['question']=questions[0].encode('utf-8')
			answers=response.xpath("//div[5]/strong/text()").extract()
			item['answer']=answers[0].encode('utf-8')
			"""str_cats=response.xpath("//a[@class='bigbtn']/text()").extract_first()
			str_cat=str_cats[0].encode('utf-8')
			karakter_sayisi=len(answers[0].encode('utf-8'))
			yield karakter_sayisi """
		yield item