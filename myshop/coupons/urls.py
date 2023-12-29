from django.urls import path
from . import views

app_name = 'coupons'  # для include в urls.py

urlpatterns = [
    path('apply/', views.coupon_apply, name='apply')
]
