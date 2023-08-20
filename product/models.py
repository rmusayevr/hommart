from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class Carousel(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="carousel_images")
    desc = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=255, allow_unicode=True, null=True, blank=True)
    image = models.FileField(upload_to="category_images")
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            related_name="parent_category", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_unique_slug(self):
        slug = slugify(self.name.
                       replace('ö', 'o').
                       replace('ş', 's').
                       replace('ü', 'u').
                       replace('ı', 'i').
                       replace('ə', 'e')
                       )
        return slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=255, allow_unicode=True, null=True, blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def get_unique_slug(self):
        slug = slugify(self.name.
                       replace('ö', 'o').
                       replace('ş', 's').
                       replace('ü', 'u').
                       replace('ı', 'i').
                       replace('ə', 'e')
                       )
        return slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    image = models.ImageField(upload_to="product_images")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.image.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, allow_unicode=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    sale_percent = models.IntegerField(default=0)
    final_price = models.FloatField(null=True, blank=True)
    in_sale = models.BooleanField(default=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='product_brand')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='product_category')
    datetime = models.DateTimeField(auto_now_add=True)
    is_popular = models.BooleanField(default=False)
    special_time = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_unique_slug(self):
        slug = slugify(self.name.
                       replace('ö', 'o').
                       replace('ş', 's').
                       replace('ü', 'u').
                       replace('ı', 'i').
                       replace('ə', 'e')
                       )
        return slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        if self.in_sale:
            self.final_price = self.price
            self.price = round((
                self.price - (self.price*(self.sale_percent/100))), 2)
        return super().save(*args, **kwargs)

    @property
    def get_product_version(self):
        for version in self.product_version.all():
            return version

    def get_absolute_url(self):
        return reverse('detail', kwargs={"product": self.slug, "version": self.get_product_version.slug})

    def __str__(self):
        return self.name


class ProductVersion(models.Model):
    version = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, allow_unicode=True, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    image = models.ManyToManyField(Image, related_name="product_images")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_version')

    class Meta:
        verbose_name = "Product Version"
        verbose_name_plural = "Product Versions"

    def get_unique_slug(self):
        slug = slugify(self.version.
                       replace('ö', 'o').
                       replace('s', 'ş').
                       replace('u', 'ü').
                       replace('ı', 'i')
                       )
        return slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.version)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name}'s {self.version} version"
