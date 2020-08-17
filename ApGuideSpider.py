import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class ApGuideSpider(scrapy.Spider):
    name = "ApGuideSpider"
    allowed_domains = [
        'www.apartmentguide.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.apartmentguide.com/apartments/Texas/Texas-City/Stone-Ridge/192470/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        TITLE_SELECTOR = 'div.dx7KI h1._3ozKD::text'
        title = response.css(TITLE_SELECTOR).extract_first().strip()
        print('title', title)
        # Recuperar html do site online em um offline
        # page = 'trulia-item'
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        