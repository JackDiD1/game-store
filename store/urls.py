from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('', views.home, name='home'),
]