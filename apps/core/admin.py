from django.contrib import admin
from django import forms
from .models import Bid, Answer, User, Category, CategoryGroup
from django.contrib.auth.admin import UserAdmin


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'group')


class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class CategoryGroupForm(forms.ModelForm):

    class Meta:
        model = CategoryGroup
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class BidAdmin(admin.ModelAdmin):
    list_display = ('author', 'unreg_email', 'author_email', 'category', 'product', 'description', 'status', 'created', 'updated')


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'bid', 'description', 'price', 'currency', 'url')


admin.site.register(Bid, BidAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)



