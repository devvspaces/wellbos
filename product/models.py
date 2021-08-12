# import inflect

from product.utils import unique_product_code
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from PIL import Image
from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import magic

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    
    def save(self):
        """Save method for Category."""
        self.slug = self.name.lower().replace(' ', '-')

        self.save()
    
    # Override save method to update slug
    def save(self, *args, **kwargs):
        if self.name:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Category."""
        return reverse('product:category', kwargs={'category': self.slug})
    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='product/category/sub', blank=True)
    desc = models.CharField(max_length=30, default="Trustworthy threads")
    description = models.TextField(default="From dress-down Fridays to weekend 'fits, our edit of men’s polo shirts knows no bounds when it comes to versatility. From long-sleeve polo shirts to short-sleeve polo tops, Wellbos DESIGN has hundreds of styles and designs to suit your unique style, or take your pick from men's designer polo shirts by Fred Perry and Polo Ralph Lauren, adding their classic logos to your smart-casual rotation. You can pair your polo T-shirt with skinny jeans, tailored shorts or even check trousers. Preppy vibes incoming.")

    def __str__(self):
        return self.name

    def save(self):
        """Save method for Category."""
        self.slug = self.name.lower().replace(' ', '-')

        self.save()
    
    # Override save method to update slug
    def save(self, *args, **kwargs):
        if self.name:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'


class ProductImage(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='product/images',max_length=500,blank=True,null=True)
    thumbnail = models.ImageField(upload_to='product/images/thumbs',max_length=500,blank=True,null=True)

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200,200)

        print(magic.from_buffer(self.image.file.read(2048), mime=True))
        print(dir(self.image.file))
        print(dir(self.image))

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.file.read()).decode("utf-8"))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self):
        # create a thumbnail
        self.create_thumbnail()

        super().save()
    
    def __str__(self):
        return self.product.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, null=True)
    brand_desc = models.TextField(default='This is WELLBOS DESIGN – your go-to for all the latest trends, no matter who you are, where you’re from and what you’re up to. Exclusive to WELLBOS, our universal brand is here for you, and comes in Plus and Tall. Created by us, styled by you.')
    code = models.CharField(max_length=10, unique=True, editable=False)
    details = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    models_height = models.CharField(max_length=15, blank=True)
    models_wearing = models.CharField(max_length=15, blank=True)

    def image_count(self):
        return self.productimage_set.count()
    
    def get_image(self):
        image = self.productimage_set.first()
        return image
    
    # THis gets the details in a list format
    def list_details(self):
        return [i.strip().capitalize() for i in self.details.split(',')]

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    stars = models.IntegerField(default=1)
    comment = models.TextField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name



# Signals
@receiver(pre_save, sender = Product)
def create_product_code(sender, instance, **kwargs):
    if bool(instance.code) == False:
        # Create a unique product code
        code = unique_product_code(instance)
        instance.code = code
        instance.save()