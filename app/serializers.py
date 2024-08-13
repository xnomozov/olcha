from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Comment, Product, Group, ProductAttribute


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


class ProductAttributeSerializer(serializers.ModelSerializer):
    class AttributeSerializer(serializers.ModelSerializer):
        attributes = serializers.SerializerMethodField()

        def get_attributes(self, products):
            attributes = ProductAttribute.objects.filter(product=products.id)
            attributes_dict = {}
            for attribute in attributes:
                attributes_dict[attribute.key.name] = attribute.value.name
            return attributes_dict

        class Meta:
            model = Product
            fields = ['id', 'name', 'slug', 'attributes']


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password2"]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError({"detail": "User already exists!"})
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"message": "Both passwords must match!"})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return data

    def create(self, validated_data):
        # Remove password2 as it is not needed for user creation
        validated_data.pop('password2')

        # Create the user
        user = User.objects.create_user(**validated_data)
        return user
