import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

class ApartmentSpider(scrapy.Spider):
    name = "ApartmentSpider"
    
    def start_requests(self):
        urls = [
            'https://www.rent.com/texas/texas-city-apartments',
            # 'https://www.rent.com/texas/texas-city-houses',
            # 'https://www.rent.com/texas/texas-city-apartments?boundingbox=-124.398,29.048,-86.825,48.873',
            # 'https://www.rent.com/texas/texas-city-apartments?boundingbox=-99.964,27.266,-62.391,47.526',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Acessar cada item da lista
        for item in response.css('._348mM._3UPGk'):
            # Entrar na página do item e extrair dados
            
            TITLE_SELECTOR_CSS = 'div._3csYd.Kv8CE._1_8Hm'
            TITLE_SELECTOR_XPATH = './/a/text()'
            item_title = item.css(TITLE_SELECTOR_CSS).xpath(TITLE_SELECTOR_XPATH).extract_first()

            PRICE_SELECTOR_CSS = 'div._3csYd.Kv8CE._1_8Hm'
            PRICE_SELECTOR_XPATH = './/span/text()'
            item_price = item.css(PRICE_SELECTOR_CSS).xpath(PRICE_SELECTOR_XPATH).extract_first()

            ADDRESS_SELECTOR_CSS = 'div._2E91L'
            ADDRESS_SELECTOR_XPATH = './/p/text()'
            item_address = item.css(ADDRESS_SELECTOR_CSS).xpath(ADDRESS_SELECTOR_XPATH).extract()
            yield {
                'title': item_title if item_title else 'None',
                'price': item_price if item_price else 'Contact for more information',
                'address': item_address[0] if item_address[0] else 'None',
                # 'neighborhood': item_neighborhood if item_neighborhood else 'None',
                # 'zip': item_zip if item_zip else 'None',
            }

        NEXT_PAGE_SELECTOR = '._qkIB a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )
        
        # Recuperar html do site online em um offline
        # page = response.url.split("-")[2]
        # print('page', page)
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)