import os
from django.conf import settings
from django.core.files import File
from django.db import models, transaction
import openpyxl
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

# 📦 Модель товара
class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=0)

    old_price = models.DecimalField(
        "Старая цена",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_new = models.BooleanField("Новинка", default=False)
    hide_price = models.BooleanField("Скрыть цену", default=False)

    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='products')

    def price_change(self):
        if self.old_price:
            if self.price < self.old_price:
                return "down"
            elif self.price > self.old_price:
                return "up"
        return None

    def __str__(self):
        return self.name

# 📁 Модель загрузки Excel файла
class ProductUpload(models.Model):
    file = models.FileField("Excel файл", upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Загрузка от {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Изображение для {self.product.name}"

#
class MenuItem(models.Model):
    title = models.CharField("Название пункта", max_length=100)
    slug = models.SlugField("Ссылка", unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)
    content = models.TextField("Содержимое страницы", blank=True)

    parent = models.ForeignKey(
            'self',
            verbose_name="Родительский пункт",
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name='children'
        )

    class Meta:
        ordering = ['order']
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню сайта"
    
    def get_url(self):
        return f"/page/{self.slug}/"

    def __str__(self):
        return self.title

# 
class PageImage(models.Model):
    page = models.ForeignKey(
        'MenuItem',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Страница"
    )
    image = models.ImageField("Изображение", upload_to='pages/')
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Изображение страницы"
        verbose_name_plural = "Изображения страниц"

    def __str__(self):
        return f"Изображение для {self.page.title}"

# 🤖 Автоматический импорт товаров из Excel после загрузки файла
@receiver(post_save, sender=ProductUpload)
def import_products_from_excel(sender, instance, created, **kwargs):
    if not created:
        return

    wb = openpyxl.load_workbook(instance.file.path)
    sheet = wb.active

    imported_names = []  # список товаров из файла

    for row in sheet.iter_rows(min_row=2, values_only=True):
        name, price, category_name = row

        if not name:
            continue

        name = str(name).strip()
        imported_names.append(name)

        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0

        product, created = Product.objects.get_or_create(name=name)

        if category_name:
            category_name = str(category_name).strip()

            category, _ = Category.objects.get_or_create(
                name=category_name,
                parent=None
            )

            product.categories.clear()
            product.categories.add(category)

        product.price = price

        product.save()

    # 🧹 Удаляем товары, которых нет в файле
    Product.objects.exclude(name__in=imported_names).delete()