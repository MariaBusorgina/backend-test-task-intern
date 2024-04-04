from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'image', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'image', 'category', )
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Subcategory, SubcategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'image_one', 'image_second', 'image_three', 'subcategory', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Product, ProductAdmin)




admin.site.site_title = 'Админ-панель магазина продуктов'
admin.site.site_header = 'Админ-панель магазина продуктов'