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


class Category(models.Model):
    """Категория"""
    name = models.CharField("Наименование категории", max_length=50, null=False, help_text="Наименование категории")
    parentCategory = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Manufacturer(models.Model):
    """Производитель"""
    name = models.CharField("Наименование производителя", max_length=100, null=False, help_text="Наименование производителя")
    address = models.CharField("Адрес", max_length=300, help_text="Адрес", null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, help_text="Телефон", null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    name = models.CharField("Наименование товара", max_length=50, null=False, help_text="Наименование товара")
    description = models.CharField("Описание товара", max_length=50, null=False, help_text="Описание товара")
    createdOn = models.DateTimeField("Дата добавления", auto_now_add=True)
    category = models.ForeignKey(Category)
    manufacturer = models.ForeignKey(Manufacturer)
    productStatus = models.IntegerField("Статус товара", choices=PRODUCT_STATUSES, default=1)
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, help_text="Стоимость")
    seller = models.ForeignKey(User)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    """Характеристики товара"""
    name = models.CharField("Наименование характеристики", max_length=50, null=False, help_text="Наименование характеристики")
    category = models.ForeignKey(Category)
    is_main = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductDetailValue(models.Model):
    """Значение характеристики товара"""
    stringValue = models.CharField("Строковое значение характеристики", max_length=250, help_text="Строковое значение характеристики")
    # product = models.ForeignKey(Product)
    productDetail = models.ForeignKey(ProductDetail)

    def __str__(self):
        return self.stringValue


class ProductPosition(models.Model):
    count = models.IntegerField("Количество товара", default=0, help_text="Количество товара")
    product = models.ForeignKey(Product)

    def __str__(self):
        return '{0}_{1}_{2}'.format(self.id, self.product, str(self.count))


class ValueProductPosition(models.Model):
    product_detail_value = models.ForeignKey(ProductDetailValue)
    product = models.ForeignKey(Product)
    product_position = models.ForeignKey(ProductPosition, null=True, blank=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.product_detail_value, self.product, self.product_position)


class Order(models.Model):
    """Заказ"""
    orderDate = models.DateTimeField("Дата заказа", auto_now_add=True, help_text="Дата заказа")
    orderStatus = models.IntegerField("Статус заказа", choices=ORDER_STATUSES, default=1)
    customer = models.ForeignKey(User, related_name="customer")
    seller = models.ForeignKey(User, related_name="seller")


class OrderPosition(models.Model):
    """Строка заказа"""
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


class ProductImage(models.Model):
    image = models.ImageField("Наименование файла", upload_to='images/products/%Y/%m/%d/')
    product = models.ForeignKey(Product)
    isMain = models.BooleanField("Основное изображение?")

