from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    methods = {
        ("online", "Onlayn ödəmə"),
        ("cash", "Qapıda nağd ödəmə"),
        ("cart", "Qapıda kartla ödəmə")
    }

    payment_method = forms.ChoiceField(label="Payment Method", widget=forms.RadioSelect(
        attrs={'id': 'form-check-input'}), choices=methods)

    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'address_link', 'payment_method']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control inputs py-2'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control inputs py-2'}),
            'address': forms.Textarea(attrs={'class': 'form-control inputs py-3 px-4',
                                             'placeholder': 'Çatdırılma ünvanı haqqında, Şəhər, Küçə, Ev',
                                             'rows': 4,
                                             'required': False}),
            'address_link': forms.TextInput(attrs={'class': 'form-control inputs py-2'}),
        }