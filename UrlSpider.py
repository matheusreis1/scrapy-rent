import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Extrair TODOS os links de imoveis
class UrlSpider(scrapy.Spider):
    name = "UrlSpider"
    
    def start_requests(self):
        # Ler todos os links do site
        links = open('cities-links-list.txt','r')
        urls = links.read().split()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Salvar todos os links de imovel
        for item in response.css('._348mM._3UPGk'):
            url = response.url
            state = url.split('/1')[0].split('com/')[1]

            URL_SELECTOR_CSS = 'div._3csYd.Kv8CE._1_8Hm a::attr(href)'
            item_url = item.css(URL_SELECTOR_CSS).extract()
            filename = 'all-links.txt'
            with open(filename, 'a') as f:
                f.write('https://rent.com/'+state+item_url[0]+'\n')
            self.log('Saved file %s' % filename)
            
        NEXT_PAGE_SELECTOR = '._qkIB a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )