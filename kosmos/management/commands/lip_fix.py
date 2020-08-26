from kosmos.models import MakeupProduct
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        lip_liners = MakeupProduct.objects.filter(product_type='lip_liner')
        for product in lip_liners:
            product.product_type = 'lip'
            product.category = 'lip_liner'
            product.save()
        lipsticks = MakeupProduct.objects.filter(product_type='lipstick')
        for product in lipsticks: 
            product.product_type = 'lip'
            product.save()