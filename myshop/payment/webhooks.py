import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body  # тело http-запроса
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(  # событие, например успешная оплата
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':  # если это платеж и он оплачен
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)  # если нет заказа ошибка
            order.paid = True  # заказ оплачен
            order.stripe_id = session.payment_intent  # сохраняем id платежа stripe
            order.save()
            payment_completed.delay(order.id)  # начать отправлять письмо

    return HttpResponse(status=200)  # говорим страйпу что получили вебхук
