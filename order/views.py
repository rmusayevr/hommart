from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from order.models import Basket, BasketItem, Wishlist, Order
from .forms import OrderForm

class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    model = Basket

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        user_basket = Basket.objects.filter(user = self.request.user.id, is_active=True).first()
        total = 0
        subtotal = 0
        sale = 0
        if user_basket:
            all_products = user_basket.items.all()
            for product in all_products:
                total += product.get_total()
                subtotal += product.get_subtotal()
                sale += product.get_sale()
            context['total'] = total
            context['subtotal'] = subtotal
            context['sale'] = sale
            context['items'] = all_products
        return context

class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = "wishlist.html"
    model = Wishlist

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        user_wishlist = Wishlist.objects.filter(user = self.request.user.id).first()
        if user_wishlist:
            all_products = user_wishlist.items.all()
            context['items'] = all_products
        return context

class CartVerifyView(LoginRequiredMixin, CreateView):
    template_name = "cart_verify.html"
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        basket = Basket.objects.filter(user=self.request.user, is_active=True).first()
        if form.cleaned_data['payment_method'] == "online":
            order = form.save(commit=False)
            order.basket = basket
            order.save()
            basket.is_active = False
            basket.save()
            return redirect('card')
        order = form.save(commit=False)
        order.basket = basket
        order.save()
        basket.is_active = False
        basket.save()
        return redirect('card_verify')

    def get_context_data(self, **kwargs):
        context = super(CartVerifyView, self).get_context_data(**kwargs)
        user_basket = Basket.objects.filter(user = self.request.user.id, is_active=True).first()
        total = 0
        subtotal = 0
        sale = 0
        if user_basket:
            all_products = user_basket.items.all()
            for product in all_products:
                total += product.get_total()
                subtotal += product.get_subtotal()
                sale += product.get_sale()
            context['total'] = total
            context['subtotal'] = subtotal
            context['sale'] = sale
        return context

def card(request):
    return render(request, "card.html")

def card_verify(request):
    return render(request, "card_verify.html")
