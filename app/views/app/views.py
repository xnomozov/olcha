# Create your views here.
from urllib import request

from django.db.models import Prefetch
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from app.models import Category, Product, Group, Image
from app.serializers import CategorySerializer, ProductSerializer, GroupSerializer, ProductAttributeSerializer
from app import permissions
Prefetch

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)


class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsSuperAdminOrReadOnly,)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'slug'


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.select_related('category')
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_object(self):
        obj = get_object_or_404(Group, slug=self.kwargs['slug'])
        if not obj:
            raise NotFound("Group not found")
        return obj





class ProductListView(generics.ListCreateAPIView):

    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsOwnerIsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('group_slug')

        queryset = Product.objects.select_related('group__category')

        if category_slug and group_slug:
            queryset = queryset.filter(group__category__slug=category_slug, group__slug=group_slug)
        elif category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        elif group_slug:
            queryset = queryset.filter(group__slug=group_slug)

        return queryset


class ProductAttributeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('group').prefetch_related('attributes__key', 'attributes__value')

    serializer_class = ProductAttributeSerializer
    lookup_field = 'slug'
