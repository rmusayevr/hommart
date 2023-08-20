from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from product.models import Category, Carousel, Product, ProductVersion
from django.db.models import Q
from .forms import SearchForm

class HomePage(ListView):
    template_name = 'index.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['carousels'] = Carousel.objects.all()
        context['chosen_items'] = Product.objects.order_by("-datetime").all()[:10]
        context['new_items'] = Product.objects.order_by("-datetime").all()[:10]
        context['special_items'] = Product.objects.filter(is_popular=True)        
        return context
    

def SearchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            product = Product.objects.filter(Q(name__icontains=name)| Q(brand__name__icontains=name))
            context = {
                'products' : product,
            }
            return render(request, 'search.html', context)
    return  HttpResponseRedirect('/')       


def ErrorView(request):
    return render(request, "error.html")