from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.translation import ugettext_lazy as _

import uuid
import datetime

from decimal import *



class User(AbstractUser):
    name = models.CharField(_('Name'), max_length=500, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), max_length=30, blank=True)
    balance = models.DecimalField(_('Balance'), default=0, decimal_places=2, max_digits=12, blank=False, validators=[MinValueValidator(Decimal('0.01'))])
    #role = models.IntegerField(default=1, blank=False)


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Предполагаем, что возможно отоброжение по id, поэтому делаем его непарсящимся
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name=_('Author'))
    unreg_phone_number = PhoneNumberField(blank=True)
    unreg_email = models.EmailField(_('Email for answer unregistered user'), max_length=30, blank=True)

    product = models.TextField(_('Product'), max_length=500, blank=False)  # TODO: ForeignKey to advanced product
    description = models.TextField(_('Description'), max_length=500, blank=True)
    category = models.ForeignKey("Category", verbose_name=_("category"), blank=True, null=True)
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
    _status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='O')  # такое через choices, иначе в админке смысла нет
    @property
    def status(self):
        return self.get__status_display
    @status.setter
    def status(self, value):
        self._status = value

    #_timeleft = models.PositiveIntegerField(_('Timeleft, sec'), default='5')

    @property
    def timeleft(self):
        calc_timeleft = self.lifetime - ((datetime.datetime.now() - self.created).seconds / 60)
        if calc_timeleft > 0:
            return calc_timeleft
        else:
            return 0

    lifetime = models.PositiveIntegerField(_('Lifetime, min'), default='5')
    created = models.DateTimeField(_('Created'), auto_now_add=True)  # Сразу добавляем текущую дату
    updated = models.DateTimeField(_('Updated'), auto_now=True)  # Сохраняем время последнего изменения

    def get_absolute_url(self):  # TODO: Убить эту дичь!
        return reverse('bid_detail', args=[str(self.id)])
    def author_email(self):
        return self.author.email
    def inform(self):
        try:
            answer = Answer.objects.filter(bid=self.id).order_by('price')[0]
        except:
            answer = None
        if answer:
            print("answer.price: {0} answer.currency: {1}".format(answer.price, answer.currency))
            message = '''
            В ходе обработки Вашей заявки поступило выгодное предложение:
            Стоимость: {0}{1}
            Продукт: {2}
            '''.format(answer.price, answer.currency, self.product)

        else:
            print("answers - none")
            message = '''
            Истекло время выполнения Вашей заявки.
            К сожалению, предложений не поступило!
            Полная стоимость заявки возвращена на Ваш аккаунт Эврики.

            Продукт: {0}
            '''.format(self.product)
        if self.unreg_email:
            email = self.unreg_email
            who = "Anonymous"
        else:
            email = self.author.email
            who = str(self.author.name)
        print("send_mail -> who: {0} email: {1}".format(who, email))
        send_mail(
            who,
            message,
            'report@eureka.com',
            [email, ],
            fail_silently=False,
        )
    def close(self):
        self.status = 'C'
        self.save()
        self.inform()

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=512)
    description = models.TextField(_("Description"), blank=True, null=True)
    group = models.ForeignKey("CategoryGroup", verbose_name=_("category group"), blank=True, null=True)

    def __str__(self):
        return self.title

class CategoryGroup(models.Model):
    title = models.CharField(_("Title"), max_length=512)
    description = models.TextField(_("Description"), blank=True, null=True)

    def __str__(self):
        return self.title

