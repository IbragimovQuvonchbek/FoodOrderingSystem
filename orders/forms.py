from django import forms


class CheckoutForm(forms.Form):
    customer_email = forms.EmailField(required=True, label="Email")
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Delivery Address")
    delivery_lat = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    delivery_lng = forms.DecimalField(widget=forms.HiddenInput(), required=False)


