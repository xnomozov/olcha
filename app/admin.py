from django.contrib import admin

from app.models import Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title',  'image']
    list_display = ['title', 'image', 'slug']
    search_fields = ['title']
