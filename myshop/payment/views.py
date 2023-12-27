from django.shortcuts import render, redirect, reverse, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)  # забираем order_id, передали его в orders/views
    order = get_object_or_404(Order, id=order_id)  # заказ по id
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {  # данные сеанса оформления платежа stripe
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,  # куда перенапрвлять после успешной/отмененной оплаты
            'cancel_url': cancel_url,
            'line_items': []  # товарные позиции
        }
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {  # инфа о цене
                    'unit_amount': int(item.price * Decimal('100')),  # в копейках
                    'currency': 'rub',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(**session_data)  # создать сеанс с переданными данными

        return redirect(session.url, code=303)

    else:  # в locals передаются все переменные функции кроме противоположных блоков (не пер. переменные из блока if)
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
