from django.db import models
from django.contrib.auth.models import AbstractUser
from colorfield.fields import ColorField
import datetime
from django.core.validators import URLValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    """related name attributes
    bag
    reviews
    collections
    hearted_collections
    """
    has_notifications = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class MakeupProduct(models.Model):
    """ related name attributes
    tags 
    colours
    reviews
    """

    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=32)
    img = models.TextField(blank=True, validators=[URLValidator()])
    link = models.TextField(blank=True, validators=[URLValidator()])
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    currency = models.CharField(max_length=4, default='CAD')
    avg_rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)

    PRODUCT_TYPES = [
        ('blush', 'Blush'),
        ('bronzer', 'Bronzer'),
        ('eyebrow', 'Eyebrow'),
        ('eyeliner', 'Eyeliner'),
        ('eyeshadow', 'Eyeshadow'),
        ('foundation', 'Foundation'),
        ('lip', 'Lip Product'),
        ('mascara', 'Mascara'),
        ('nail_polish', 'Nail Polish')
    ]

    product_type = models.CharField(choices=PRODUCT_TYPES, max_length=32)

    CATEGORIES = [
        ('powder', 'Powder'),
        ('cream', 'Cream'),
        ('pencil', 'Pencil'),
        ('liquid', 'Liquid'),
        ('gel', 'Gel'),
        ('palette', 'Palette'),
        ('contour', 'Contour'),
        ('bb_cc', 'BB/CC'),
        ('concealer', 'Concealer'),
        ('mineral', 'Mineral'),
        ('highlighter', 'Highlighter'),
        ('lipstick', 'Lipstick'),
        ('lip_gloss', 'Lip Gloss'),
        ('lip_stain', 'Lip Stain'),
        ('lip_liner', 'Lip Liner'),
        ('none', 'N/A')
    ]

    

    category = models.CharField(choices=CATEGORIES, max_length=16)
    expiry = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # calculate how long each product lasts in months based on personal experience
        if self.expiry == 0:
            if self.category == 'powder' or self.product_type == 'lip_liner' or self.product_type == 'lipstick':
                self.expiry = 24
            elif self.category == 'concealer' or self.category == 'cream' or self.product_type == 'eyeshadow' or self.product_type == 'foundation' or self.product_type == 'nail_polish':
                self.expiry = 12
            elif self.product_type == 'eyeliner':
                if self.category == 'pencil':
                    self.expiry = 24
                else:
                    self.expiry = 6
            elif self.product_type == 'mascara':
                self.expiry = 4
            else:
                self.expiry = 6
        
        return super(MakeupProduct, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.brand + '\'s ' + self.name

class Tag(models.Model):
    TAG_CHOICES = [
        ('alcohol free', 'Alcohol-Free'),
        ('Canadian', 'Canadian'),
        ('CertClean', 'CertClean'),
        ('Chemical Free', 'Chemical-Free'),
        ('cruelty free', 'Cruelty-Free'),
        ('Dairy Free', 'Dairy-Free'),
        ('EWG Verified', 'EWG Verified'),
        ('EcoCert', 'EcoCert'),
        ('Fair Trade', 'Fair Trade'),
        ('Gluten Free', 'Gluten-Free'),
        ('Hypoallergenic', 'Hypoallergenic'),
        ('Natural', 'Natural'),
        ('No Talc', 'No Talc'),
        ('Non-GMO', 'Non-GMO'),
        ('oil free', 'Oil-Free'),
        ('Organic', 'Organic'),
        ('Peanut Free', 'Peanut-Free'),
        ('purpicks', 'Purpicks'),
        ('silicone free', 'Silicone-Free'),
        ('Sugar Free', 'Sugar-Free'),
        ('USDA Organic', 'USDA Organic'),
        ('Vegan', 'Vegan'),
        ('water free', 'Water-Free'),
        ('CUSTOM', 'User-Made')
    ]
    name = models.CharField(choices=TAG_CHOICES, max_length=32)
    tagged_product = models.ForeignKey(MakeupProduct, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return str(self.tagged_product) + ' tag: ' + self.name

class Colour(models.Model):
    name = models.CharField(max_length=32)
    hex_value = ColorField(default='#FF0000')
    product = models.ForeignKey(MakeupProduct, on_delete=models.CASCADE, related_name='colours')

    def __str__(self):
        return self.name

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(MakeupProduct, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    STAR_CHOICES = [
        (i, i) for i in range(1, 6)
    ] # ratings from 1-5 stars

    stars = models.IntegerField(choices=STAR_CHOICES)

    def __str__(self):
        return 'Review on ' + str(self.product) + ' by ' + str(self.author)

class MakeupBag(models.Model):
    """ related name attributes
    items
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bag')
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.owner) + '\'s Makeup Bag'

class MakeupBagItem(models.Model):
    bag = models.ForeignKey(MakeupBag, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MakeupProduct, on_delete=models.CASCADE)
    open_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    expiry = models.DateField(blank=True, null=True, default=datetime.date.today)
    notes = models.TextField(blank=True) # consider removing
    notifications = models.BooleanField(verbose_name='Notify When Expired', default=True)
    is_expired = models.BooleanField(default=False) # will always be false for those with notifications=False

    def save(self, *args, **kwargs):
        if not self.id: # saving for the first time
            if self.expiry == self.open_date or self.expiry < self.open_date: # expiry date is same as open date, or is before open date
                self.expiry = self.open_date + datetime.timedelta(days=self.product.expiry*30)
            print('open' + str(self.open_date))
            print('hi' + str(self.expiry))
        if str(self.expiry) == str(datetime.date.today()):
            self.is_expired = True
        if self.is_expired:
            user = self.bag.owner
            if not user.has_notifications:
                user.has_notifications = True
                user.save()
        return super(MakeupBagItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.product) + ' in ' + str(self.bag)

class Collection(models.Model):
    """related name attributes
    items
    hearts
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    public = models.BooleanField(default=False)
    title = models.CharField(max_length=32)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True) # update every time modified
    banner_num = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(11)])

    def __str__(self):
        return self.title + ' Collection by ' + str(self.author)

class CollectionItem(models.Model):
    product = models.ForeignKey(MakeupProduct, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return str(self.product) + ' in ' + str(self.collection)

class CollectionHeart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hearted_collections')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='hearts')

    def __str__(self):
        return str(self.collection) + ' hearted by ' + str(self.user)