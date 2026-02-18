from django.contrib import admin
from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem, PageImage


# 🔹 Inline изображения товаров
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# 🔹 Inline изображения страниц
class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1


# 🔹 Массовое назначение категории
@admin.action(description="Назначить категорию")
def assign_category(modeladmin, request, queryset):
    category_id = request.POST.get('category')

    if category_id:
        category = Category.objects.get(id=category_id)
        for product in queryset:
            product.categories.add(category)


# 🔹 Админка товаров (всё в одном месте)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'is_new')
    list_editable = ('price', 'old_price', 'is_new')

    filter_horizontal = ('categories',)
    search_fields = ('name',)
    actions = [assign_category]

    inlines = [ProductImageInline]


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