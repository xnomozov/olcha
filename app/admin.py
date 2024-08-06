from django.contrib import admin

from app.models import Category, Product, Group


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image']
    list_display = ['title', 'image', 'slug']
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'image', 'description', 'price', 'group', 'discount']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ['name', 'image', 'category']
