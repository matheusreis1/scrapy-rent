import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class ApRatingSpider(scrapy.Spider):
    name = "ApRatingSpider"
    allowed_domains = [
        'www.apartmentratings.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.apartmentratings.com/ca/los-angeles/1022-tiverton_9199332346275147276/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('response', response)
        # Recuperar html do site online em um offline
        page = 'aprating-item'
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        