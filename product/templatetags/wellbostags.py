from django import template
from django.template.defaultfilters import stringfilter

from product.models import Category

register=template.Library()

# Code to get the category list
@register.simple_tag()
def get_category():
	return Category.objects.all()