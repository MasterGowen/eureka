from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import MinValueValidator

import uuid
from decimal import *


class User(AbstractUser):
    name = models.CharField(max_length=500, blank=True)  # Имя - это не текст, это строка!
    phone_number = models.CharField(max_length=30, blank=True) # Не надо транслита, никаких tel, это нечитаемо в коде!
    email = models.EmailField(max_length=30, blank=True)  # Email - всегда EmailField!
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12, blank=False, validators=[MinValueValidator(Decimal('0.01'))])  # Деньги - всегда DecimalField!
    #role = models.IntegerField(default=1, blank=False)


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Предполагаем, что возможно отоброжение по id, поэтому делаем его непарсящимся
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    product = models.TextField(max_length=500, blank=False)  # TODO: ForeignKey to advanced product
    description = models.TextField(max_length=500, blank=True)
    # answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True)
    STATUSES = (
        ('O', "Opened"),
        ('R', 'Running'),
        ('C', 'Closed'),
        ('S', 'Succefully closed'),
        ('P', 'Protest'),
        ('A', 'Protest analysis'),
        ('E', 'Protestly closed')
    )
    status = models.CharField(max_length=1, choices=STATUSES, default='O')  # такое через choices, иначе в админке смысла нет
    created = models.DateTimeField(auto_now_add=True)  # Сразу добавляем текущую дату
    updated = models.DateTimeField(auto_now=True)  # Сохраняем время последнего изменения

    def get_absolute_url(self):  # TODO: Убить эту дичь!
        return '/'


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=False)
    description = models.TextField(max_length=500, blank=False)
    status = models.IntegerField(default=0)  # 0 - актуальный 1- не актуальный
    price = models.DecimalField(default=0, decimal_places=2, max_digits=12, blank=False,  validators=[MinValueValidator(Decimal('0.01'))])
    CURRENCIES = (
        ('rur', 'RUR'),
        ('usd', 'USD'),
        ('eur', 'Euro'),
    )
    currency = models.CharField(choices=CURRENCIES, default='rur', max_length=3)
    url = models.URLField(max_length=2048, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)  # Сразу добавляем текущую дату


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
