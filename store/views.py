from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .models import MenuItem
from django.shortcuts import get_object_or_404

def product_list(request):
    type_name = request.GET.get('type')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    # Главные категории
    main_categories = Category.objects.filter(parent__isnull=True)

    selected_main = None
    subcategories = Category.objects.none()

    # Фильтр по главной категории
    if type_name:
        selected_main = Category.objects.filter(
            name=type_name,
            parent__isnull=True
        ).first()

        if selected_main:
            subcategories = selected_main.children.all()
            products = products.filter(categories__parent=selected_main)

    # Фильтр по подкатегории
    if category_id:
        products = products.filter(categories__id=category_id)

    products = products.distinct().order_by('name')

    return render(request, 'store/product_list.html', {
        'products': products,
        'main_categories': main_categories,
        'subcategories': subcategories,
        'selected_main': selected_main,
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