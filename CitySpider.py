import scrapy
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Pegar todas as cidades de todos os estados
# Montar todos os links possiveis do site, 
# Juntando estado+cidade+houses/apartments
class CitySpider(scrapy.Spider):
    name = "CitySpider"
    
    def start_requests(self):
        urls = [
            'https://www.rent.com/alabama',
            'https://www.rent.com/alaska',
            'https://www.rent.com/arizona',
            'https://www.rent.com/arkansas',
            'https://www.rent.com/california',
            'https://www.rent.com/colorado',
            'https://www.rent.com/connecticut',
            'https://www.rent.com/delaware',
            'https://www.rent.com/district-of-columbia',
            'https://www.rent.com/florida',
            'https://www.rent.com/georgia',
            'https://www.rent.com/hawaii',
            'https://www.rent.com/idaho',
            'https://www.rent.com/illinois',
            'https://www.rent.com/indiana',
            'https://www.rent.com/iowa',
            'https://www.rent.com/kansas',
            'https://www.rent.com/kentucky',
            'https://www.rent.com/louisiana',
            'https://www.rent.com/maine',
            'https://www.rent.com/maryland',
            'https://www.rent.com/massachusetts',
            'https://www.rent.com/michigan',
            'https://www.rent.com/minnesota',
            'https://www.rent.com/mississippi',
            'https://www.rent.com/missouri',
            'https://www.rent.com/montana',
            'https://www.rent.com/nebraska',
            'https://www.rent.com/nevada',
            'https://www.rent.com/new-hampshire',
            'https://www.rent.com/new-jersey',
            'https://www.rent.com/new-mexico',
            'https://www.rent.com/new-york',
            'https://www.rent.com/north-carolina',
            'https://www.rent.com/north-dakota',
            'https://www.rent.com/ohio',
            'https://www.rent.com/oklahoma',
            'https://www.rent.com/oregon',
            'https://www.rent.com/pennsylvania',
            'https://www.rent.com/rhode-island',
            'https://www.rent.com/south-carolina',
            'https://www.rent.com/south-dakota',
            'https://www.rent.com/tennessee',
            'https://www.rent.com/texas',
            'https://www.rent.com/utah',
            'https://www.rent.com/vermont',
            'https://www.rent.com/virginia',
            'https://www.rent.com/washington',
            'https://www.rent.com/west-virginia',
            'https://www.rent.com/wisconsin',
            'https://www.rent.com/wyoming',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('.col-lg-4'):
            url = response.url
            state = url.split('/1')[0].split('com/')[1]

            cities = item.css('li a::text').extract()
            filename = 'cities-links-list.txt'

            for city in cities:
                city_name = city.lower().replace(' ', '-')
                with open(filename, 'a') as f:
                    f.write('https://www.rent.com/'+state+'/'+city_name+'-apartments\n')
                    f.write('https://www.rent.com/'+state+'/'+city_name+'-houses\n')
                self.log('Saved file %s' % filename)        