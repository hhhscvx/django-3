from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()  # с какого числа действует
    valid_to = models.DateTimeField()  # до какого числа действует
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    active = models.BooleanField()  # действует ли

    def __str__(self):  # что будет отображаться на админ сайте
        return self.code
