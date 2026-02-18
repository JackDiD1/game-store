from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .models import MenuItem
from django.db.models import F
from django.db import models
from django.shortcuts import redirect

def product_list(request):
    type_name = request.GET.get('type', 'Новинки')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    main_categories = Category.objects.filter(parent__isnull=True)

    selected_main = None
    subcategories = Category.objects.none()

    # 🔹 Фильтр по главной категории
    if type_name:
        selected_main = Category.objects.filter(
            name__iexact=type_name,
            parent__isnull=True
        ).first()

        if selected_main:
            subcategories = selected_main.children.all()
            products = products.filter(categories__parent=selected_main)

    # 🔹 Подкатегория
    if category_id:
        products = products.filter(categories__id=category_id)

    # 🔹 Если категория Новинки → показываем только is_new
    if type_name.lower() == "новинки":
        products = products.filter(is_new=True)

    # 🔹 Если категория Изменения цен
    if type_name.lower() == "изменения цен":
        products = products.filter(
            old_price__isnull=False
        ).exclude(old_price=F('price'))

    products = products.distinct().order_by('name')

    menu_items = MenuItem.objects.filter(is_active=True)

    return render(request, 'store/product_list.html', {
        'products': products,
        'main_categories': main_categories,
        'subcategories': subcategories,
        'selected_main': selected_main,
        'menu_items': menu_items,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    menu_items = MenuItem.objects.filter(is_active=True)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'menu_items': menu_items,
    })


def page_detail(request, slug):
    menu_items = MenuItem.objects.filter(is_active=True)
    page = get_object_or_404(MenuItem, slug=slug)

    return render(request, 'store/page_detail.html', {
        'page': page,
        'menu_items': menu_items,
    })

def redirect_to_new(request):
    return redirect('/products/?type=Новинки')