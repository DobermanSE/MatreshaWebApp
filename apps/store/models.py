from django.db import models
from django.contrib.auth.models import User
# Необходимы для ограничения диапазона значений IntegerField
# from django.core.validators import MinValueValidator, MaxValueValidator


# Статус товара
PRODUCT_STATUSES = (
    (1, "Модерация"),
    (2, "Активный")
)


# Статус заказа
ORDER_STATUSES = (
    (1, "В обработке"),
    (2, "Активный")
)


# Категория
class Category(models.Model):
    name = models.CharField("Наименование категории", max_length=50, null=False, help_text="Наименование категории")
    parentCategory = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Производитель
class Manufacturer(models.Model):
    name = models.CharField("Наименование производителя", max_length=100, null=False, help_text="Наименование производителя")
    address = models.CharField("Адрес", max_length=300, help_text="Адрес", null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, help_text="Телефон", null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)

    def __str__(self):
        return self.name


# Товар
class Product(models.Model):
    name = models.CharField("Наименование товара", max_length=50, null=False, help_text="Наименование товара")
    description = models.CharField("Описание товара", max_length=50, null=False, help_text="Описание товара")
    createdOn = models.DateTimeField("Дата добавления", auto_now_add=True)
    category = models.ForeignKey(Category)
    manufacturer = models.ForeignKey(Manufacturer)
    productStatus = models.IntegerField("Статус товара", choices=PRODUCT_STATUSES, default=1)
    # TODO: переделать на ImageField
    # https://docs.djangoproject.com/es/1.9/topics/files/
    # mainImage = models.ForeignKey(File)
    seller = models.ForeignKey(User)

    def __str__(self):
        return self.name


# Характеристики товара
class ProductDetail(models.Model):
    name = models.CharField("Наименование характеристики", max_length=50, null=False, help_text="Наименование характеристики")
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name


# Значение характеристики товара
class ProductDetailValue(models.Model):
    stringValue = models.CharField("Строковое значение характеристики", max_length=250, help_text="Строковое значение характеристики")
    product = models.ForeignKey(Product)
    productDetail = models.ForeignKey(ProductDetail)

    def __str__(self):
        return self.stringValue


# Заказ
class Order(models.Model):
    orderDate = models.DateTimeField("Дата заказа", auto_now_add=True, help_text="Дата заказа")
    orderStatus = models.IntegerField("Статус заказа", choices=ORDER_STATUSES, default=1)
    customer = models.ForeignKey(User, related_name="customer")
    seller = models.ForeignKey(User, related_name="seller")


# Строка заказа
class OrderPosition(models.Model):
    quantity = models.IntegerField("Количество", help_text="Количество")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, help_text="Стоимость")
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)


# TODO: вынести комментарии и рейтинг в отдельное приложение (не забыть про import в начале файла)
# Рейтинг
# class Rating(models.Model):
#     value = models.IntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])
#     createdOn = models.DateTimeField("Дата создания", auto_now_add=True)
#     product = models.ForeignKey(Product)
#     createdBy = models.ForeignKey(User)
#
#
# # Комментарий
# class Comment(models.Model):
#     text = models.CharField("Стоимость", max_length=300, null=False, help_text="Текст комментария")
#     createdOn = models.DateTimeField("Дата создания", auto_now_add=True)
#     product = models.ForeignKey(Product)
#     createdBy = models.ForeignKey(User)

# TODO: переделать на ImageField или FilelField
# Файл
# class File (models.Model):
#     name = models.CharField("Наименование файла", max_length=100, null=True, help_text="Наименование файла")
#     contentType = models.CharField(max_length=30, null=False)
#     content = models.BinaryField()
#     product = models.ForeignKey(Product)
