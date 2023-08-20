from django.views.generic import ListView, DetailView
from product.models import Product, ProductVersion, Image, Category, Brand
from django.db.models import Q, Count, Sum, Case, When, Value, IntegerField
from django.utils.translation import get_language_info, get_language


class ProductsView(ListView):
    model = Product
    template_name = "products.html"
    paginate_by = 8
    context_object_name = "products"

    def get_queryset(self):
        child = self.request.GET.get("child")
        category = self.request.GET.get("category")
        if child:
            return Product.objects.filter(category__slug=child).order_by("-datetime").all()
        elif category:
            return Product.objects.filter(category__parent__slug=category).order_by("-datetime").all()
        return Product.objects.order_by("-datetime").all()

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        child = self.request.GET.get("child")
        category = self.request.GET.get("category")
        if child:
            context['child'] = Category.objects.get(slug=child)
        elif category:
            context['category'] = Category.objects.get(slug=category)
        
        context['categories'] = Category.objects._mptt_filter(parent=None).annotate(product_count=Count('parent_category__product_category'))
        context['subcategories'] = Category.objects.exclude(parent=None).annotate(product_count=Count('product_category'))
        context['brands'] = Brand.objects.all().annotate(product_count=Count('product_brand'))
        return context


class ProductDetailView(DetailView):
    template_name = 'detail.html'
    model = Product
    context_object_name = "product"

    def get_object(self):
        return ProductVersion.objects.filter(product__slug=self.kwargs.get("product"), slug=self.kwargs.get("version")).first()

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['images'] = Image.objects.all()
        product = Product.objects.get(slug=self.kwargs.get("product"),
                                      product_version__slug=self.kwargs.get("version"))
        context['versions'] = ProductVersion.objects.filter(
            product__name=product.name)
        context['r_items'] = Product.objects.filter(Q(brand__name=kwargs['object'].product.brand) | Q(category__name=kwargs['object'].product.category), ~Q(
            product_version__slug=self.kwargs.get("slug")), ~Q(name=kwargs["object"].product.name)).all()
        return context
