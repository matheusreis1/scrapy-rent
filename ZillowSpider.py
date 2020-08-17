import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class ZillowSpider(scrapy.Spider):
    name = "ZillowSpider"
    allowed_domains = [
        'www.zillow.com'
    ]

    def start_requests(self):
        urls = [
            'https://www.zillow.com/homes/for_sale/Texas-City-TX/2085999619_zpid/47966_rid/globalrelevanceex_sort/29.570471,-94.694596,29.237278,-95.163575_rect/10_zm/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('response', response)
        # TITLE_SELECTOR = 'div.h3.pan.man.defaultLineHeight.noWrap.overflowEllipsis::text'
        # title = response.css(TITLE_SELECTOR).extract_first().strip()
        # print('title', title)
        # Recuperar html do site online em um offline
        page = 'zillow-item'
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        