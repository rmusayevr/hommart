from modeltranslation.translator import register, TranslationOptions
from .models import ProductVersion, Product, Category, Carousel


@register(Carousel)
class CarouselTranslationOptions(TranslationOptions):
    fields = ('name', 'desc')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(ProductVersion)
class ProductVersionTranslationOptions(TranslationOptions):
    fields = ('version', )
