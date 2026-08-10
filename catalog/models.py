from django.db import models

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"