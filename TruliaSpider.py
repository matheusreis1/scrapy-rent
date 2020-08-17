import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class TruliaSpider(scrapy.Spider):
    name = "TruliaSpider"
    allowed_domains = [
        'www.trulia.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.trulia.com/p/tx/texas-city/2810-6th-ave-n-texas-city-tx-77590--1126111267',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        TITLE_SELECTOR = 'div.h3.pan.man.defaultLineHeight.noWrap.overflowEllipsis::text'
        title = response.css(TITLE_SELECTOR).extract_first().strip()
        print('title', title)
        # Recuperar html do site online em um offline
        # page = 'trulia-item'
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        