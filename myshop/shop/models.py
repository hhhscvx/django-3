from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=144)
    slug = models.SlugField(max_length=144, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # по absolute_url попадаешь в список продуктов этой категории
        return reverse('shop:product_list_by_category', args=[self.slug])  # и передается slug для шаблона


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='product',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=144)
    slug = models.SlugField(max_length=144)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,  # макс. кол-во цифр (включая после запятой)
                                decimal_places=2)  # кол-во цифр после запятой
    available = models.BooleanField(default=True)  # в наличии ли товар
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',  # связывает по absolute_url с шаблонов product_detail
                       args=[self.id, self.slug])  # и передает id и slug данного продукта для шаблона
