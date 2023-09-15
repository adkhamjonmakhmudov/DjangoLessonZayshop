from django.contrib import admin
from django.utils.html import format_html

from apps.models import Product, Category, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ctg_image',)
    exclude = ('slug',)
    readonly_fields = ('created_at',)

    @admin.display(description='Image')
    def ctg_image(self, obj: Category):
        return format_html(
            f'<img style="border-radius: 15px; width:120px; height:80px;" src="{obj.picture.url}" alt="{obj.name}">')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_image', 'short_desc', 'price', 'size', 'color', 'category')
    exclude = ('created_at', 'slug',)
    readonly_fields = ('created_at', 'view_count')

    @admin.display(description='Image')
    def product_image(self, obj: Product):
        return format_html(
            f'<img style="border-radius: 15px; width:120px; height:80px;" src="{obj.image.url}" alt="{obj.name}">')


admin.site.register(User)
