from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """Задание по отправке уведомления по эл.почте при успешном оформлении заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order.id}'
    message = f'{order.first_name},\n\nВаш заказ успешно оформлен. Номер заказа - {order.id}'
    mail_sent = send_mail(subject, message, 'admin@myshop.com',
                          [order.email])  # отправить на email того, кто оформлял заказ
    return mail_sent
