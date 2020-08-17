import scrapy

class HouseSpider(scrapy.Spider):
    name = "HouseSpider"
    
    def start_requests(self):
        urls = [
            'https://www.rent.com/texas/dallas-apartments/the-wilson-reviews-5-4929771',
            # 'https://www.rent.com/texas/dallas-apartments/the-wilson-4-4929771',
            # 'https://www.rent.com/alabama/alabaster-apartments/the-view-apartment-homes-4-100017784',
            # 'https://www.rent.com/texas/texas-city-apartments',
            # 'https://www.rent.com/texas/texas-city-houses',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print('response', response.css('._348mM._3UPGk').get())

        # for item in response.css('._348mM._3UPGk'):

        #     PRICE_SELECTOR_CSS = 'div._3csYd.Kv8CE._1_8Hm'
        #     PRICE_SELECTOR_XPATH = './/span/text()'
        #     item_price = item.css(PRICE_SELECTOR_CSS).xpath(PRICE_SELECTOR_XPATH).extract_first()

        #     yield {
        #         'price': item_price,
        #     }

        # NEXT_PAGE_SELECTOR = '._qkIB a::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # print('next page', next_page)
        # if next_page:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback = self.parse
        #     )
        filename = 'quotes-reviews-house-item.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)