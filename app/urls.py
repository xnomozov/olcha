from . import views
from django.urls import path, include

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('category-create/', views.CreateCategoryView.as_view(), name='category-create'),
    path('category/<slug:slug>/update/', views.UpdateCategoryView.as_view(), name='category-update'),
    path('category/<slug:slug>/delete/', views.DeleteCategoryView.as_view(), name='category-delete'),
]
