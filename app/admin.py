from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import Category, Product, Group, Comment, Image


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'get_image']
    list_display = ['title', 'get_image', 'slug']
    search_fields = ['title']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50' height='50'>")

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'group', 'discount', 'user_like']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ['name', 'image', 'category']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['rating', 'product', 'user', 'comment']
    readonly_fields = ['user']  # Optionally make the user field read-only

    def save_model(self, request, obj, form, change):
        if not change:  # Only set user on creation, not on updates
            obj.user = request.user
        super().save_model(request, obj, form, change)


# Register the admin class with the Comment model
admin.site.register(Comment, CommentAdmin)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['is_primary', 'image', 'product']
