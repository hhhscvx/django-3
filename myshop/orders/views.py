from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,  # для каждого товара создается OrderItem
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # очистить корзину после заполнения данных
            # запустить асинхронное задание (во время создания заказа начинает делаться сообщение об успешном заказе)
            order_created.delay(order.id)
            request.session['order_id'] = order.id  # сохраняем в сессии пользователя номер заказа
            return redirect(reverse('payment:process'))  # payment - это namespace
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required  # is_active и is_staff запрашивающего пользователя равны True
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required  # требует чтоб был авторизован админ
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',  # генерирует html код для pdf используя шаблон pdf.html
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')  # объект ответа Django в pdf типе
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'  # имя файла
    weasyprint.HTML(string=html).write_pdf(response,  # генерируем pdf из указанного html с исп. указанного css
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'css/pdf.css')])
    return response
