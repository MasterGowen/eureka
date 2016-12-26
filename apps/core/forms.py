from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['category', 'product', 'description', 'lifetime', 'unreg_email']  # 'unreg_phone_number',