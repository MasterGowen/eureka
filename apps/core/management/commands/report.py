from django.core.management.base import BaseCommand, CommandError
from apps.core.models import Bid, Answer
from django.core.mail import send_mail
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):

        bids = Bid.objects.filter(status__exact='O', created__lte=datetime.datetime.now() - datetime.timedelta(seconds=60 * 5))

        for bid in bids:
            bid.status = 'C'
            print(bid.id, 'status updated!')
            bid.save()

            answer = Answer.objects.filter(bid=bid.id).order_by('price')[0]

            message = '''

            В ходе обработки Вашей заявки поступило выгодное предложение:

            Стоимость: {0}{1}

            Продукт: {2}

            '''.format(answer.price, answer.currency,  bid.product)

            send_mail(
                str(bid.author.name),
                message,
                'n.v.ignatchenko@urfu.ru',
                [bid.author.email, ],
                fail_silently=False,
            )

