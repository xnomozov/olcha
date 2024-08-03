from . import views
from django.urls import path, include

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
]
