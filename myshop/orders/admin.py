from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])  # args передаем в представление
    return mark_safe(f'<a href="{url}">Смотреть</a>')  # url на детальный просмотр заказа


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if
              not field.many_to_many and not field.one_to_many]  # все поля кроме many_to_many и one_to_many
    writer.writerow([field.verbose_name for field in fields])  # заголовки = поля для заполнения
    for obj in queryset:  # переход по каждому выбранному чекбоксом объекту
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)  # извлекаем объект и name всех его полей
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')  # если дата то задать дату как строку
            data_row.append(value)  # значение добавляется в этот список и экспортируется в csv
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_stripe_payment.short_description = 'Stripe payment'


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])  # url из представления admin_order_pdf
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Счет'  # название столбца на админ сайте


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_stripe_payment, 'created', 'updated',
                    order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
