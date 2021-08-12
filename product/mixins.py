from django.http.response import Http404
from django.shortcuts import get_object_or_404

from .models import Category, SubCategory

class ParseKwargs(object):
    def parse_link(self):
        category = self.kwargs.get('category')
        sub = self.kwargs.get('sub')

        # Get the category and sub category instance
        category = get_object_or_404(Category, slug__exact=category)

        try:
            sub_category = category.subcategory_set.get(slug__exact=sub)
        except SubCategory.DoesNotExist:
            raise Http404

        return category,sub_category