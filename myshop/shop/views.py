from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)  # достаем только товары в наличии
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = get_object_or_404(Product, slug=category_slug)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)  # продукт по указанным параметрам+в наличии
    return render(request,
                  'shop/product/detail.html',
                  {'product': product})
