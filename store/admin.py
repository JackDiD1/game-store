from django.contrib import admin
from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem, PageImage
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

class AssignCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Выберите категорию"

def assign_category(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = AssignCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            count = 0
            for product in queryset:
                product.categories.add(category)
                count += 1

            modeladmin.message_user(
                request,
                f"Категория назначена {count} товарам"
            )
            return HttpResponseRedirect(request.get_full_path())

    else:
        form = AssignCategoryForm(
            initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}
        )

    return render(
        request,
        'admin/assign_category.html',
        {'products': queryset, 'form': form}
    )

assign_category.short_description = "Назначить категорию"

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