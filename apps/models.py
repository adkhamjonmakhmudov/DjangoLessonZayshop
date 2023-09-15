from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model
from django.utils.text import slugify
from django_resized import ResizedImageField


class Product(models.Model):
    class SizeChoices(models.TextChoices):
        M = 'm', 'M'
        L = 'l', 'L'
        X = 'x', 'X'
        X_L = 'x_l', 'XL'

    class ColorChoices(models.TextChoices):
        RED = 'red', 'Red'
        BLACK = 'black', 'Black',
        WHITE = 'white', 'White'
        BLUE = 'blue', 'Blue'

    name = models.CharField(max_length=50)
    image = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='products/%m', blank=True,
                              null=True, default='linux-dark-hacking-operating-system-wallpaper-preview.jpeg')
    image1 = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='products/%m', blank=True,
                               null=True)
    image2 = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='products/%m', blank=True,
                               null=True)
    image3 = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='products/%m', blank=True,
                               null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    view_count = models.BigIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=10, choices=SizeChoices.choices, blank=True, null=True)
    color = models.CharField(max_length=255, choices=ColorChoices.choices, blank=True, null=True)
    category = models.ForeignKey('apps.Category', on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def short_desc(self):
        return self.description[:30] + ' ...'

    def update_views(self, *args, **kwargs):
        self.view_count = self.view_count + 1
        super().save(*args, **kwargs)
        return self.view_count

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # NOQA
            while Category.objects.filter(slug=self.slug).exists():
                slug = Category.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self.name:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:  # noqa
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'
            super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=30)
    picture = ResizedImageField(size=[350, 200], crop=['middle', 'center'], upload_to='category/images',
                                default='b1547ea47c41ff923ae45c9373c88ad7.jpg')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # NOQA
            while Category.objects.filter(slug=self.slug).exists():
                slug = Category.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self.name:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:  # noqa
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'
            super().save(*args, **kwargs)


class User(AbstractUser):
    phone_number = models.CharField(max_length=14)
    image = ResizedImageField(crop=[300, 300], upload_to='users/photos/%m')
