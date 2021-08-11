
from django.shortcuts import render
from django.views.generic import TemplateView

class ProductList(TemplateView):
    template_name = 'product/product-list.html'
    extra_context = {
        'title': 'Men'
    }