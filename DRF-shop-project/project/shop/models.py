from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='images/category/%Y/%m/%d/', verbose_name='Изображение', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='images/subcategory/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory', verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    image_one = models.ImageField(upload_to='images/products/%Y/%m/%d/', verbose_name='Изображение 1', blank=True)
    image_second = models.ImageField(upload_to='images/products/%Y/%m/%d/', verbose_name='Изображение 2', blank=True)
    image_three = models.ImageField(upload_to='images/products/%Y/%m/%d/', verbose_name='Изображение 3', blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='product', verbose_name='Подкатегория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket', verbose_name='Пользователь')

    @property
    def all_total_price(self):
        total_price = sum(i.total_price for i in self.basket_item.all())
        return total_price

    @property
    def all_total_number(self):
        total_number = sum(i.quantity for i in self.basket_item.all())
        return total_number

    def __str__(self):
        return self.user.username


class BasketItem(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')

    @property
    def total_price(self):
        total_price = self.quantity * self.price
        return total_price

    def __str__(self):
        return f"{self.product.title} - {self.quantity} уп."
