from rest_framework import serializers
from .models import Category, Comment, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
