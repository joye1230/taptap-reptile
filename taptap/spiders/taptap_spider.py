#coding=utf-8
import scrapy
import time
import re

blocklist = ("<p class=\"comment-item-title\">官方回复",
      "Daily global top game recommendation, No Cheating, No Advertising",
      "Game from official source, No Piracy, No Modification",
      "Integrate game ranking data from the world's major platform",
)
def is_blocklist(word):
    for block in blocklist:
        if re.match(block, word):
            return True
    return False

class QuotesSpider(scrapy.Spider):
    name = "taptap"



    allowed_domains = ["taptap.com"]
    def start_requests(self):
        for i in range(1,28):
            yield scrapy.Request(url = 'https://www.taptap.com/app/10538/review?order=default&page=%d#review-list'%i, callback=self.parse)


    def parse(self, response):
        output=open(r'out.txt','a')   #打开文件
        # for body in response.css('div.item-text-body'):
        body = response.css('div.item-text-body')[0]
        body2 = body.xpath('//ul//p')
        for body3 in body2:
            comment = body3.extract().encode("utf-8")
            comment = comment.replace('<p>','')
            comment = comment.replace('</p>','')
            if is_blocklist(comment):
                continue
            output.write(comment+"\n")
        output.close()

        #     yield {
        #         'text': quote.css('span.text::text').extract_first(),
        #         'author': quote.css('small.author::text').extract_first(),
        #         'tags': quote.css('div.tags a.tag::text').extract(),
        #     }
