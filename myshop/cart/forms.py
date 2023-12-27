from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]  # int для математического и тп. а str для отображения


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(  # ограничен типом данных, в данном случае int
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int)  # choices это диапазон
    override = forms.BooleanField(  # True если пользователь сам впишет свое количество
        required=False,  # не обязательно заполнять
        initial=False,  # по умолчанию False
        widget=forms.HiddenInput)  # не будет показываться пользователю
