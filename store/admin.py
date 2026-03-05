from django.contrib import admin, messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Product, Category, ProductUpload, ProductImage
from .models import MenuItem, PageImage


# ---------- INLINE ----------

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1


# ---------- ACTION: добавить категории ----------

@admin.action(description="Добавить категории товарам")
def add_categories(modeladmin, request, queryset):

    if "apply" in request.POST:

        category_ids = request.POST.getlist("categories")

        if not category_ids:
            modeladmin.message_user(
                request,
                "Категории не выбраны",
                level=messages.ERROR
            )
            return HttpResponseRedirect(request.get_full_path())

        categories = Category.objects.filter(id__in=category_ids)

        for product in queryset:
            product.categories.add(*categories)

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
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        }
    )


# ---------- ACTION: удалить категории ----------

@admin.action(description="Удалить категории у товаров")
def remove_categories(modeladmin, request, queryset):

    if "apply" in request.POST:

        category_ids = request.POST.getlist("categories")

        categories = Category.objects.filter(id__in=category_ids)

        for product in queryset:
            product.categories.remove(*categories)

        modeladmin.message_user(
            request,
            f"Категории удалены у {queryset.count()} товаров"
        )

        return HttpResponseRedirect(request.get_full_path())

    categories = Category.objects.all()

    return render(
        request,
        "admin/remove_categories.html",
        {
            "products": queryset,
            "categories": categories,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        }
    )


# ---------- ACTION: новинка ----------

@admin.action(description="Сделать товары новинками")
def mark_new(modeladmin, request, queryset):

    queryset.update(is_new=True)

    modeladmin.message_user(
        request,
        f"{queryset.count()} товаров отмечены как новинки"
    )


# ---------- ACTION: убрать новинку ----------

@admin.action(description="Убрать отметку новинки")
def unmark_new(modeladmin, request, queryset):

    queryset.update(is_new=False)

    modeladmin.message_user(
        request,
        f"{queryset.count()} товаров больше не новинки"
    )


# ---------- ACTION: скрыть цену ----------

@admin.action(description="Скрыть цену")
def hide_price(modeladmin, request, queryset):

    queryset.update(hide_price=True)

    modeladmin.message_user(
        request,
        f"Цена скрыта у {queryset.count()} товаров"
    )


# ---------- ACTION: показать цену ----------

@admin.action(description="Показать цену")
def show_price(modeladmin, request, queryset):

    queryset.update(hide_price=False)

    modeladmin.message_user(
        request,
        f"Цена показана у {queryset.count()} товаров"
    )


# ---------- PRODUCT ADMIN ----------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "price", "old_price", "is_new", "hide_price")

    filter_horizontal = ("categories",)

    list_filter = ("categories", "is_new")

    search_fields = ("name",)

    inlines = [ProductImageInline]

    actions = [
        add_categories,
        remove_categories,
        mark_new,
        unmark_new,
        hide_price,
        show_price,
    ]


# ---------- MENU ----------

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display = ("title", "parent", "order", "is_active")

    list_editable = ("order", "is_active")

    list_filter = ("parent",)

    prepopulated_fields = {"slug": ("title",)}

    inlines = [PageImageInline]


# ---------- OTHER ----------

admin.site.register(Category)
admin.site.register(ProductUpload)