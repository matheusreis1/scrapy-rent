import scrapy
import json
from selenium import webdriver
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Extrair dados de dentro dos itens
class ItemSpider(scrapy.Spider):
    name = "ItemSpider"
    allowed_domains = [
        'www.rent.com'
    ]

    def start_requests(self):
        # Ler todos os links do site
        # links = open('all-links.txt','r')
        # urls = links.read().split()
        urls = [
            # 'https://www.rent.com/texas/dallas-apartments/the-merc-4-680157'
            # 'https://www.rent.com/texas/texas-city-houses/411-6th-ave-n-4-r2947377',
            'https://www.rent.com/texas/dallas-apartments/the-wilson-4-4929771',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.extract_first())
        items = []

        # Url
        item_url = response.url

        # Title
        TITLE_SELECTOR = 'div.pdp-heading h1.pdp-heading-name span::text'
        item_title = response.css(TITLE_SELECTOR).extract_first()

        # Address
        MAP_SELECTOR = 'div.pdp-neighborhood-map'
        LATITUDE_SELECTOR = 'div.map::attr(data-latitude)'
        item_address_latitute = response.css(MAP_SELECTOR).css(LATITUDE_SELECTOR).extract_first()

        LONGITUDE_SELECTOR = 'div.map::attr(data-longitude)'
        item_address_longitude = response.css(MAP_SELECTOR).css(LONGITUDE_SELECTOR).extract_first()

        LOCALITY_ADDRESS_SELECTOR = 'div.pdp-heading div.pdp-heading-info div.pdp-heading-address span'
        item_address = response.css(LOCALITY_ADDRESS_SELECTOR)
        item_adress_dict = {}
        item_street_address = ''
        item_address_locality = ''
        item_address_region = ''
        item_address_postal_code = ''
        for i,item in enumerate(item_address):
            SELECTOR = 'span::text'
            if i == 1:
                item_street_address = item.css(SELECTOR).extract_first()
            elif i == 2:
                item_address_locality = item.css(SELECTOR).extract_first()
            elif i == 3:
                item_address_region = item.css(SELECTOR).extract_first()
            elif i == 4:
                item_address_postal_code = item.css(SELECTOR).extract_first()

            item_adress_dict.update({
                'street': item_street_address,
                'locality': item_address_locality,
                'region': item_address_region,
                'postal_code': item_address_postal_code,
                'latitude': item_address_latitute,
                'longitude': item_address_longitude
            })

        # Price
        PRICE_SELECTOR = 'div.pdp-heading-meta span.pdp-heading-meta-rent.bold::text'
        item_price = response.css(PRICE_SELECTOR).extract_first()
        
        # Type
        TYPE_SELECTOR = 'div.pdp-heading-meta span.pdp-heading-meta-beds::text'
        item_beds = response.css(TYPE_SELECTOR).extract_first()

        # Pets
        PETS_SELECTOR = 'div.pdp-heading-meta span.pdp-heading-meta-pets::text'
        item_pets = response.css(PETS_SELECTOR).extract_first()

        # Phone
        PHONE_SELECTOR = 'div.pdp-heading-meta span.pdp-heading-meta-phone.hidden-xs a strong::text'
        item_phone = response.css(PHONE_SELECTOR).extract_first()

        # Images
        IMAGES_SELECTOR = 'section#pdp-contact-top div.block-body.clearfix div.carousel-col div.carousel.has-photos.pdp-image-container div.carousel-picture.pdp-image'
        item_images = response.css(IMAGES_SELECTOR)

        item_photos = []
        for image in item_images:
            SELECTOR = 'img::attr(src)'
            url = image.css(SELECTOR).extract_first()
            if url:
                item_photos.append(url)
            else:
                SELECTOR = 'img::attr(data-lazy-src)'
                url = image.css(SELECTOR).extract_first()
                item_photos.append(url)
        
        # Floorplans (for)

        FLOORPLANS_SELECTOR = 'section#pdp-contact-top div.block-body.clearfix div.carousel-col div.lead-body section#pdp-ula-floorplans div.block-body div.floorplans.clearfix details.floorplan-group'
        item_floorplans = response.css(FLOORPLANS_SELECTOR)
        floorplans = []
        for i,item in enumerate(item_floorplans):
            NAME_SELECTOR = 'div.floorplan-group-text::text'
            list_name = item.css(NAME_SELECTOR).extract_first().replace(' ','').lower()
            
            floorplans.append({
                'name': list_name,
                'items': []
            })

            SELECTOR_DETAILS = 'div.floorplans-container div.floorplan-row'
            details = item.css(SELECTOR_DETAILS)

            for x,line in enumerate(details):
                row_dict = {}
                line_ellipsis = ''
                line_rent = ''
                line_bed_bath = ''
                line_sqft = ''
                line_availability = ''

                ELLIPSIS_SELECTOR = 'div.floorplan-item.hidden-xs.hidden-sm a::text'
                line_ellipsis = line.css(ELLIPSIS_SELECTOR).extract_first()
                if not line_ellipsis:
                    ELLIPSIS_SELECTOR = 'div.floorplan-item.floorplan-name a::text'
                    line_ellipsis = line.css(ELLIPSIS_SELECTOR).extract_first()

                RENT_SELECTOR = 'div.floorplan-item.floorplan-rent::text'
                line_rent = line.css(RENT_SELECTOR).extract_first()
                
                BED_BATH_SELECTOR = 'div.floorplan-item.floorplan-bed-bath::text'
                line_bed_bath = line.css(BED_BATH_SELECTOR).extract_first()
                
                SQFT_SELECTOR = 'div.floorplan-item.floorplan-sqft::text'
                line_sqft = line.css(SQFT_SELECTOR).extract_first()
                
                AVAILABILITY_SELECTOR = 'div.floorplan-item.floorplan-availability span::text'
                line_availability = line.css(AVAILABILITY_SELECTOR).extract_first()
                row_dict.update({
                    'ellipsis': line_ellipsis,
                    'rent': line_rent,
                    'bed_bath': line_bed_bath,
                    'sqft': line_sqft,
                    'availability': line_availability,
                })
                floorplans[i]['items'].append(row_dict)
                
        # Amenities (for)
        # Salvar em outro objeto dentro do documento
        AMENITIES_SELECTOR = 'section#pdp-amenities div.block-body div.amenity-group'
        item_amenities = response.css(AMENITIES_SELECTOR)
        amenities = []
        for i,row in enumerate(item_amenities):
            ROW_NAME_SELECTOR = 'h3::text'
            row_name = row.css(ROW_NAME_SELECTOR).extract_first().split(':')[0]

            amenities.append({
                'name': row_name,
                'items': []
            })

            ITEMS_SELECTOR = 'div div span span::text'
            amenities_extract = row.css(ITEMS_SELECTOR).extract()

            ITEMS_P_SELECTOR = 'div p::text'
            contact_details = row.css(ITEMS_P_SELECTOR).extract_first()

            if amenities_extract:    
                for item in amenities_extract:
                    amenities[i]['items'].append(item)
            elif contact_details:
                amenities[i]['items'].append(contact_details)
            else:
                ITEMS_SELECTOR = 'div::text'
                amenities_extract = row.css(ITEMS_SELECTOR).extract_first()
                amenities[i]['items'].append(amenities_extract)


        # Property Details (for)
        property_details = {}
        PROPERTY_DETAILS_DESCRIPTION_SELECTOR = 'section#pdp-details div.block-body div p::text'
        item_property_details_description = response.css(PROPERTY_DETAILS_DESCRIPTION_SELECTOR).extract_first()

        PROPERTY_DETAILS_HEADERS_SELECTOR = 'section#pdp-details div.block-body h3::text'
        item_property_headers = response.css(PROPERTY_DETAILS_HEADERS_SELECTOR).extract()
        
        PROPERTY_DETAILS_TEXTS_SELECTOR = 'section#pdp-details div.block-body p::text'
        item_property_texts = response.css(PROPERTY_DETAILS_TEXTS_SELECTOR).extract()
        list_details = []
        for i,item in enumerate(item_property_headers):
            for x, it in enumerate(item_property_texts):
                if i == x-1:
                    list_details.append({
                        'title': item,
                        'text': it
                    })

        property_details.update({
            'description': item_property_details_description if item_property_details_description else 'None',
            'details': list_details
        })
        
        # Contact Property
        CONTACT_SELECTOR = 'section#pdp-contact-bottom div.block-body div div.col-sm-12.col-md-6.col-md-pull-6.col-lg-6.col-lg-pull-5 div.contact-bottom-details'
        contact_items = response.css(CONTACT_SELECTOR)
        item_contact_items = {}
        if contact_items:
            for item in contact_items:
                DIV_SELECTOR = 'div.hidden-xs.hidden-sm p a strong::text'
                phone_number = item.css(DIV_SELECTOR).extract_first()

                CONTACT_MANAGER_SELECTOR = 'div'
                XPATH = './/div[h4/text() = "Managed by"]'
                manager = item.css(CONTACT_MANAGER_SELECTOR).xpath(XPATH)
                manager_name = manager.css('p::text').extract_first()

                OFFICE_HOURS_SELECTOR = 'div.office-hours p::text'
                office_hours = item.css(OFFICE_HOURS_SELECTOR).extract()

                MANAGER_PHOTO_SELECTOR = './/div[@itemtype="https://www.schema.org/Organization"]'
                MANAGER_PHOTO_SELECTOR_CSS = 'img::attr(data-src)'
                photo_url = item.xpath(MANAGER_PHOTO_SELECTOR).css(MANAGER_PHOTO_SELECTOR_CSS).extract_first()

                item_contact_items.update({
                    'manager_name': manager_name if manager_name else 'None',
                    'office_hours': office_hours if office_hours else 'None',
                    'manager_phone_number': phone_number if phone_number else 'None',
                    'manager_photo': photo_url if photo_url else 'None'
                })

            
        # Reviews (for e nextpage)
        # REVIEWS_URL_SELECTOR = 'section#pdp-reviews div.block-body a.btn.btn-primary.see-more-reviews::attr(href)'
        # item_reviews_link = response.css(REVIEWS_URL_SELECTOR).extract_first()
        # print('link', item_reviews_link)
        # if item_reviews_link:
        #     yield scrapy.Request(
        #         url='https://www.rent.com'+item_reviews_link, 
        #         callback=self.parse_reviews
        #         )
        reviews = []
        REVIEWS_SELECTOR = 'div#individual-reviews div.individual-review.clearfix'
        reviews_list = response.css(REVIEWS_SELECTOR)
        for review_row in reviews_list:
            review = {}
            RESIDENT_NAME_SELECTOR = 'div.resident-info h3.resident-name span::text'
            resident_name = review_row.css(RESIDENT_NAME_SELECTOR).extract_first()

            OVERALL_SATISFACTION_SELECTOR = 'div.rating-star-box div::attr(class)'
            overall_satisfaction = review_row.css(OVERALL_SATISFACTION_SELECTOR).extract_first()[-1:]
            
            COMMENT_SELECTOR = 'div.review-section p.review-text.minimize span.blurb::text'
            comment = review_row.css(COMMENT_SELECTOR).extract_first()

            DATE_REVIEW_SELECTOR = 'div.review-section p.review-text.minimize span.review-date::text'
            date = review_row.css(DATE_REVIEW_SELECTOR).extract_first()

            INDIVIDUAL_OVERALLS_SELECTOR = 'div.individual-rating-categories ul.ratings-column'
            individual_overalls = review_row.css(INDIVIDUAL_OVERALLS_SELECTOR)
            separate_overalls = []
            for column in individual_overalls:
                LI_SELECTOR = 'li'
                rows = column.css(LI_SELECTOR)
                
                for i,row in enumerate(rows):
                    row_overall = {}
                    title_individual = ''
                    value_individual = ''
                    SELECTOR = 'li span.ratings-category-label::text'
                    title_individual = column.css(SELECTOR).extract()[i]

                    VALUE_SELECTOR = 'li span.ratings-category-label strong::text'
                    value_individual = column.css(VALUE_SELECTOR).extract()[i]
                    row_overall.update({
                        'title': title_individual,
                        'value': value_individual
                    })
                    separate_overalls.append(row_overall)

            review.update({
                'resident': resident_name,
                'overall_satisfaction': overall_satisfaction,
                'comment': comment,
                'date': date,
                'individual_overall': separate_overalls,
            })
            reviews.append(review)

        # Nearby Cities
        NEARBY_CITIES_TITLE_SELECTOR = 'section#pdp-nearby-cities div.block-body div.grid.grid-gutter-md div.col-sm-3 ul li a::text'
        nearby_cities_titles = response.css(NEARBY_CITIES_TITLE_SELECTOR).extract()

        NEARBY_CITIES_URL_SELECTOR = 'section#pdp-nearby-cities div.block-body div.grid.grid-gutter-md div.col-sm-3 ul li a::attr(href)'
        nearby_cities_urls = response.css(NEARBY_CITIES_URL_SELECTOR).extract()

        list_nearby_cities = []
        for i, title in enumerate(nearby_cities_titles):
            for x, url in enumerate(nearby_cities_urls):
                if i == x:
                    list_nearby_cities.append({
                        'title': title,
                        'url': 'https://www.rent.com'+url
                    })

        # Nearby Properties
        NEARBY_PROPERTIES_TITLE_SELECTOR = 'section#pdp-similar div.block-body'
        nearby_properties_titles = response.css(NEARBY_PROPERTIES_TITLE_SELECTOR).extract()
        # print('asda', nearby_properties_titles)

        items.append({
            'url': item_url if item_url else 'None',
            'title': item_title if item_title else 'None',
            'address': item_adress_dict if item_adress_dict else 'None',
            'price': item_price if item_price else 'None',
            'beds': item_beds if item_beds else 'None',
            'pets': item_pets if item_pets else 'None',
            'phone': item_phone if item_phone else 'None',
            'images': item_photos if item_photos else 'None',
            'floorplans': floorplans if floorplans else 'None',
            'amenities': amenities if amenities else 'None',
            'property_details': property_details if property_details else 'None',
            'contact': item_contact_items if item_contact_items else 'None',
            'reviews': reviews if reviews else 'None',
            'nearby_cities': list_nearby_cities if list_nearby_cities else 'None',
            'nearby_properties': '',
        })

        with open('personal0.json', 'a') as json_file:
            for item in items:
                json.dump(item, json_file)
    
    def parse_reviews(self, response):
        print('response', response)
        reviews = []
        REVIEWS_SELECTOR = 'div#individual-reviews div.individual-review.clearfix'
        reviews_list = response.css(REVIEWS_SELECTOR)
        for review in reviews_list:
            RESIDENT_NAME_SELECTOR = 'div.resident-info h3.resident-name span::text'
            resident_name = review.css(RESIDENT_NAME_SELECTOR).extract_first()
            # print('residente', resident_name)

        NEXT_PAGE_SELECTOR = '.paging'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()
        print('next page', next_page)
        # if next_page:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback = self.parse_reviews
        #     )
        # print('reviews', reviwes_list)
