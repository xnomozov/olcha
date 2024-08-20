from app.views.app import views
from app.views.auth import views as auth_views
from django.urls import path
from root import token_vieww

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', views.CategoryDetail.as_view(), name='category-detail'),
    path('category-create/', views.CreateCategoryView.as_view(), name='category-create'),
    path('category/<slug:slug>/update/', views.UpdateCategoryView.as_view(), name='category-update'),
    path('category/<slug:slug>/delete/', views.DeleteCategoryView.as_view(), name='category-delete'),
    path('category/<slug:category_slug>/<slug:group_slug>/', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/product/attributes/', views.ProductAttributeView.as_view(), name='product-attributes'),
    # path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),

    # group
    path('category/<slug:slug>/groups/', views.GroupListView.as_view(), name='group-list'),

    # auth
    path("login/", token_vieww.LoginView.as_view(), name="user_login"),
    path("register/", token_vieww.RegisterView.as_view(), name="user_register"),
    path("logout/", token_vieww.LogoutView.as_view(), name="user_logout")
]
