# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Category


class CategoryList(APIView):
    def get(self, request, format=None):
        data = [{'title': category.title,
                 'image': request.build_absolute_uri(category.image.url)
                 } for category in Category.objects.all()]

        return Response(data)
