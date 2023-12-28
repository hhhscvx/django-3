from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """Задание для отправки эл.письма при оплате"""
    order = Order.objects.get(id=order_id)
    subject = f'Магазин - счет по заказу {order.id}'
    message = 'Счет по вашему заказу.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()  # хранение pdf файла до того как он будет прикреплен к письму
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',  # прикрепляем к письму pdf файл
                 out.getvalue(), 'application/pdf')
    email.send()
