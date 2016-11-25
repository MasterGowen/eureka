from django.contrib import admin
from django import forms
from .models import Bid, Answer, User
from django.contrib.auth.admin import UserAdmin


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = '__all__'


class BidAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'description', 'status', 'created', 'updated')


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'bid', 'description', 'price', 'currency', 'url')


admin.site.register(Bid, BidAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(User, UserAdmin)



