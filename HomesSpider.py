import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class HomesSpider(scrapy.Spider):
    name = "HomesSpider"
    allowed_domains = [
        'www.homes.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.homes.com/property/2205-11th-ave-n-texas-city-tx-77590/id-500019391664/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('response', response.url)
        TITLE_SELECTOR = 'h1.property-info__subtitle.subtitle.address.sa-child.sa-child--1'
        title = response.css(TITLE_SELECTOR)
        print('title', title)
        # Recuperar html do site online em um offline
        # page = 'homes-item'
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        