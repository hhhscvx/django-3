from django.shortcuts import render, redirect
from .forms import CouponApplyForm
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,  # code = code (ignore case)
                                        valid_from__lte=now,  # `действителен с` lower than now
                                        valid_to__gte=now,  # `действителен до` grower than now
                                        active=True)  # действителен
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None  # купон не найден
    return redirect('cart:cart_detail')  # вернуть в корзину с примененным купоном
