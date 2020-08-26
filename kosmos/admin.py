from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(MakeupProduct)
admin.site.register(Tag)
admin.site.register(Colour)
admin.site.register(Review)
admin.site.register(MakeupBag)
admin.site.register(MakeupBagItem)
admin.site.register(Collection)
admin.site.register(CollectionItem)
admin.site.register(CollectionHeart)