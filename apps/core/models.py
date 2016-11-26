from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import MinValueValidator

from django.utils.translation import ugettext_lazy as _

import uuid
from decimal import *


class User(AbstractUser):
    name = models.CharField(_('Name'), max_length=500, blank=True)  # Имя - это не текст, это строка!
    phone_number = models.CharField(_('Phone number'), max_length=30, blank=True) # Не надо транслита, никаких tel, это нечитаемо в коде!
    email = models.EmailField(_('Email'), max_length=30, blank=True)  # Email - всегда EmailField!
    balance = models.DecimalField(_('Balance'), default=0, decimal_places=2, max_digits=12, blank=False, validators=[MinValueValidator(Decimal('0.01'))])  # Деньги - всегда DecimalField!
    #role = models.IntegerField(default=1, blank=False)


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Предполагаем, что возможно отоброжение по id, поэтому делаем его непарсящимся
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name=_('Author'))
    product = models.TextField(_('Product'), max_length=500, blank=False)  # TODO: ForeignKey to advanced product
    description = models.TextField(_('Description'), max_length=500, blank=True)
    # answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True)
    STATUSES = (
        ('O', _("Opened")),
        ('R', _('Running')),
        ('C', _('Closed')),
        ('S', _('Succefully closed')),
        ('P', _('Protest')),
        ('A', _('Protest analysis')),
        ('E', _('Protestly closed'))
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='O')  # такое через choices, иначе в админке смысла нет
    created = models.DateTimeField(_('Created'), auto_now_add=True)  # Сразу добавляем текущую дату
    updated = models.DateTimeField(_('Updated'), auto_now=True)  # Сохраняем время последнего изменения

    def get_absolute_url(self):  # TODO: Убить эту дичь!
        return reverse('bid_detail', args=[str(self.id)])


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name=_('Author'))
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=False, verbose_name=_('Bid'))
    description = models.TextField(_('Description'), max_length=500, blank=False)
    status = models.IntegerField(_('Status'), default=0)  # 0 - актуальный 1- не актуальный
    price = models.DecimalField(_('Price'), default=0, decimal_places=2, max_digits=12, blank=False,  validators=[MinValueValidator(Decimal('0.01'))])
    CURRENCIES = (
        ('rur', _('₽')),
        ('usd', _('$')),
        ('eur', _('€')),
    )
    currency = models.CharField(_('Currency'), choices=CURRENCIES, default='rur', max_length=3)
    #city =
    #address =
    url = models.URLField(_('URL'), max_length=2048, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True)  # Сразу добавляем текущую дату
    updated = models.DateTimeField(_('Updated'), auto_now=True)



class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Аналогично заявке, суровый айдишник
    initiator = models.ForeignKey(User, related_name="initiator_user", blank=False)
    respondent = models.ManyToManyField(User, related_name="respondent_users", blank=True)
    bid = models.ForeignKey(Bid, blank=False)
    answer = models.ManyToManyField(Answer, blank=True)


class Order(models.Model):
    sender = models.IntegerField(blank=False)
    recipient = models.IntegerField(blank=False)
    date = models.DateTimeField()
    amount = models.FloatField(default=0, blank=False)


class Bank(models.Model):
    freeze = models.FloatField(default=0, blank=False) #not 'freese'!
