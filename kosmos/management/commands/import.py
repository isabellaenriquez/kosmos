import requests
import json
from kosmos.models import MakeupProduct, Tag, Colour
from django.core.management.base import BaseCommand

IMPORT_URL = 'https://makeup-api.herokuapp.com/api/v1/products.json'

class Command(BaseCommand):
    def import_product(self, data):
        name = data.get('name', None)
        brand = data.get('brand', 'Unknown')
        img = data.get('image_link', None)
        link = data.get('product_link', None)
        description = data.get('description', 'No description available.')
        price = data.get('price', '0.00')
        currency = data.get('currency', 'CAD')
        product_type = data.get('product_type', None)
        category = data.get('category', 'none')
        if category is None: # when null is returned for some reason
            category = 'none'
        if description is None:
            description = 'No description available'
        if brand is None:
            brand = 'Unknown'
        else: # title case
            brand = brand.title()
        if price is None:
            price = '0.00'
        if currency is None:
            currency = 'CAD'

        p, created = MakeupProduct.objects.get_or_create(name=name, brand=brand, img=img, link=link, description=description, price=price, \
            currency=currency, product_type=product_type, category=category)

        #p = MakeupProduct(name=name, brand=brand, img=img, link=link, description=description, price=price, \
        #    currency=currency, product_type=product_type, category=category)
        if created: # hasn't been uploaded to database before
            p.save()

            # tags list
            tags = data.get('tag_list', None)
            if len(tags) > 0:
                for tag in tags:
                    if tag == 'Peanut Free Product':
                        tag = 'Peanut Free'
                    t = Tag(name=tag, tagged_product=p)
                    t.save()

            #colours
            colours = data.get('product_colors', None)
            if len(colours) > 0:
                for colour in colours: # color is a dictionary
                    name = colour['colour_name']
                    if name is None:
                        name = colour['hex_value']
                    c = Colour(name=name, hex_value=colour['hex_value'], product=p)
                    c.save()

    def handle(self, *args, **options):
        # make GET request to API
        response = requests.get(url=IMPORT_URL)
        response.raise_for_status()
        data = response.json()
        for data_object in data:
            self.import_product(data_object)