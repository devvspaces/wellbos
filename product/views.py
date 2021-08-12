from django.http.response import Http404
from product.mixins import ParseKwargs
from product.models import Category, Product, SubCategory
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView


class CategorySubList(TemplateView):
    template_name = 'product/category-sub-list.html'
    extra_context = {
        'title': ''
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the category
        category = self.kwargs.get('category')
        category = get_object_or_404(Category, slug__exact=category)
        context["title"] = category.name.capitalize()
        context["category"] = category.slug

        # Get the sublist
        context['sublist'] = category.subcategory_set.all()

        return context
    
class ProductList(ListView, ParseKwargs):
    template_name = 'product/product-list.html'
    extra_context = {
    }
    model = Product

    def custom_queryset(self, category, sub_category):
        return Product.objects.filter(category=category, sub_category=sub_category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Identify the page
        category, sub_category = self.parse_link()

        context["title"] = f"{category.name.capitalize()}\'s {sub_category.name.capitalize()}"

        # Get the products with the category and sub category
        queryset = self.custom_queryset(category, sub_category)
        context["products"] = queryset
        context["total_count"] = queryset.count()
        context["category"] = category
        context["sub_category"] = sub_category

        return context


class ProductDetail(TemplateView, ParseKwargs):
    template_name = 'product/product-detail.html'
    extra_context = {
    }
    model = Product

    def get_object(self):
        category, sub_category = self.parse_link()
        queryset = Product.objects.filter(category=category, sub_category=sub_category)
        # Get the product in the above query set or return 404
        try:
            return queryset.get(code=self.kwargs.get('code'))
        except Product.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the product
        product = self.get_object()

        context["title"] = product.name.capitalize()
        context['product'] = product

        return context
    