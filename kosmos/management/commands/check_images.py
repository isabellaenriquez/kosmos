import requests
from kosmos.models import MakeupProduct
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def img_exists(self, url): # check if image exists
        r = requests.head(url)
        return r.status_code == 200

    def handle(self, *args, **options):
        products = MakeupProduct.objects.all()
        for product in products:
            if product.img != '':
                valid_img = self.img_exists(product.img)
                if not valid_img: # image does not exist, remove link
                    product.img = ''  
                    product.save()
                    print('image was not valid') 