from django.contrib import admin
from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem
from .models import PageImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    filter_horizontal = ('categories',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('parent',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageImageInline]

admin.site.register(Category)
admin.site.register(ProductUpload)