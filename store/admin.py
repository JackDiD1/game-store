from django.contrib import admin
from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem, PageImage
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages

@admin.action(description="Добавить категории товарам")
def add_categories(modeladmin, request, queryset):

    if 'apply' in request.POST:

        category_ids = request.POST.getlist("categories")

        if not category_ids:
            modeladmin.message_user(request, "Категории не выбраны", level=messages.ERROR)
            return HttpResponseRedirect(request.get_full_path())

        categories = Category.objects.filter(id__in=category_ids)

        for product in queryset:
            for category in categories:
                product.categories.add(category)

        modeladmin.message_user(
            request,
            f"Категории добавлены {queryset.count()} товарам"
        )

        return HttpResponseRedirect(request.get_full_path())

    categories = Category.objects.all()

    return render(
        request,
        "admin/add_categories.html",
        {
            "products": queryset,
            "categories": categories,
            "action_checkbox_name": admin.ACTION_CHECKBOX_NAME,
        },
    )

# 🔹 Inline изображения товаров
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# 🔹 Inline изображения страниц
class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1

# 🔹 Админка товаров
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'is_new', 'hide_price')
    filter_horizontal = ('categories',)
    list_filter = ('categories',)
    search_fields = ('name',)
    inlines = [ProductImageInline]
    actions = [add_categories]


# 🔹 Админка меню
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('parent',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageImageInline]


# 🔹 Остальные модели
admin.site.register(Category)
admin.site.register(ProductUpload)