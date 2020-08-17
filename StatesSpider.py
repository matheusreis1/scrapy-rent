import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todos os estados do site rent.com
class StatesSpider(scrapy.Spider):
    name = "StatesSpider"
    
    def start_requests(self):
        urls = [
            'https://www.rent.com/search-by-state',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('.unstyled.col-sm-3'):
            print('state', item.css('li a::text').extract())
            estates = item.css('li a::text').extract()
            filename = 'state-list.txt'

            for estate in estates:
                print('city', estate)
                # Entrar e descobrir todas as cidades
                with open(filename, 'a') as f:
                    estate_name = estate.lower().replace(' ', '-')
                    f.write('https://www.rent.com/'+estate_name +'\n')
                self.log('Saved file %s' % filename)
        
        # Recuperar html do site online em um offline
        # page = 'states'
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        