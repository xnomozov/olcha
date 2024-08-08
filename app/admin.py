from django.contrib import admin

from app.models import Category, Product, Group, Comment, Image


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image']
    list_display = ['title', 'image', 'slug']
    search_fields = ['title']


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