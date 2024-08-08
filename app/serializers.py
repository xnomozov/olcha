from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Comment, Product, Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        avg_rating = obj.comments.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating, 1) if avg_rating is not None else 0

    def get_image(self, obj):
        request = self.context.get('request')
        try:
            image = obj.images.get(is_primary=True)

            return request.build_absolute_uri(image.image.url)
        except obj.images.model.DoesNotExist:
            return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            users = obj.user_like.all()
            return users.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = Product
        exclude = ('user_like',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)
