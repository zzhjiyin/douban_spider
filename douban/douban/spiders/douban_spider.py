# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250/']

    def parse(self, response):
        movie_list = response.xpath('//div[@id="content"]//div[@class="article"]//ol[@class="grid_view"]/li')
        for movie_item in movie_list:
            douban_item = DoubanItem()
            douban_item['movie_rank'] = movie_item.xpath('.//div[@class="item"]//em/text()').extract_first()
            douban_item['movie_name'] = movie_item.xpath('.//div[@class="item"]//div[@class="hd"]/a/span[1]/text()').extract_first()
            intro = movie_item.xpath('.//div[@class="item"]//div[@class="info"]/div[@class="bd"]/p[1]/text()').extract()
            for i_intro in intro:
                intro_s = "".join(i_intro.split())
                douban_item['movie_introduce'] = intro_s
            douban_item['movie_stars'] = movie_item.xpath('.//div[@class="item"]//div[@class="info"]//div[@class="star"]/span[2]/text()').extract_first()
            douban_item['movie_comments'] = movie_item.xpath('.//div[@class="item"]//div[@class="info"]//div[@class="star"]/span[4]/text()').extract_first()
            douban_item['movie_describe'] = movie_item.xpath('.//div[@class="item"]//div[@class="info"]//p[@class="quote"]/span[1]/text()').extract_first()
            yield douban_item

        next_url = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_url:
            next_url = next_url[0]
            yield scrapy.Request("https://movie.douban.com/top250/"+ next_url,callback = self.parse,dont_filter=True)




