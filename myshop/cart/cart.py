from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """Инициализировать корзину"""
        self.session = request.session  # текущая сессия
        cart = self.session.get(settings.CART_SESSION_ID)  # данные корзины из объекта сессии, если ее нет - None
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # если корзины нет создать пустую
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):  # quantity кол-во товара
        """Добавить товар в корзину либо обновить его количество"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,  # если товара не было в корзине то его кол-во в корзине равно нулю
                                     'price': str(product.price)}
        if override_quantity:  # если вручную меняешь кол-во товара то кол-во товара в корзине устанавливается заданным числом
            self.cart[product_id]['quantity'] = quantity
        else:  # либо прибавляется по 1 если жмешь плюсик
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True  # данные в сессии были изменены

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Прокрутить товарные позиции корзины в цикле и получить товары из БД"""
        product_ids = self.cart.keys()  # ключи корзины это id товаров
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()  # создаем копию для итерации чтобы не менять ориг словарь
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Все товары в корзине"""
        return sum(item['quantity'] for item in self.cart.values())  # Итерируем все товары и считаем сумму их количеств

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Удалить корзину из сеанса"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
