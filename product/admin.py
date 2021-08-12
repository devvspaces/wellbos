from django.contrib import admin

from .models import Category, SubCategory, Product, ProductImage, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sub_category', 'price', 'code', 'image_count')
    list_filter = ('category', 'sub_category', 'active', 'created',)
    search_fields = ('name',)

    inlines = [
        ProductImageInline,
    ]

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
