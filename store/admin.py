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

# 🔹 Админка товаров (всё в одном месте)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'is_new', 'hide_price')
#    list_editable = ('price', 'old_price', 'is_new', 'hide_price')

    filter_horizontal = ('categories',)

    list_filter = ('categories',)
    search_fields = ('name',)

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