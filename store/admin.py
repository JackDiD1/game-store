from django.contrib import admin
from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem, PageImage
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

# 🔥 Action массового назначения категории
def assign_category(modeladmin, request, queryset):
    if 'apply' in request.POST:
        category_id = request.POST.get('category')
        selected = request.POST.getlist('_selected_action')

        if category_id:
            category = Category.objects.get(pk=category_id)
            products = Product.objects.filter(pk__in=selected)

            for product in products:
                product.categories.add(category)

            modeladmin.message_user(request, "Категория назначена.")
            return HttpResponseRedirect(request.get_full_path())

    categories = Category.objects.all()

    return render(request, "admin/assign_category.html", {
        "products": queryset,
        "categories": categories,
        "action_checkbox_name": admin.ACTION_CHECKBOX_NAME,
    })

assign_category.short_description = "Назначить категорию"


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
    actions = [assign_category]


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