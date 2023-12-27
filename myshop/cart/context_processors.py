from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}  # корзина теперь доступна во всех шаблонах по переменной cart
