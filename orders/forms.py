from django import forms

class CheckoutForm(forms.Form):
    customer_email = forms.EmailField(label="Your Email", max_length=100)
