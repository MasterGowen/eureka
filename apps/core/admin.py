from django.contrib import admin
from django import forms
from .models import Bid

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = '__all__'


class BidAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'description', 'status')

admin.site.register(Bid, BidAdmin)



