from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .models import MenuItem
from django.shortcuts import get_object_or_404

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    type_filter = request.GET.get('type')

    products = Product.objects.all()

    if type_filter == 'disks':
        products = products.filter(categories__name='Диски')

    elif type_filter == 'consoles':
        products = products.filter(categories__name='Консоли')

    elif type_filter == 'accessories':
        products = products.filter(categories__name='Аксессуары')

    # Поиск по названию
    if query:
        products = products.filter(name__icontains=query)

    # Фильтр по категории
    if category_id:
        products = products.filter(categories__id=category_id)

    products = products.order_by('name')

    categories = Category.objects.all()

    menu_items = MenuItem.objects.filter(is_active=True)

    return render(request, 'store/product_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
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