from django.urls import path
from . import views
from django.shortcuts import redirect

def redirect_to_new(request):
    return redirect('/products/?type=Новинки')

urlpatterns = [
    path('', views.redirect_to_new),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]