from django.core.management.base import BaseCommand, CommandError
from apps.core.models import Bid, Answer
from django.core.mail import send_mail

from django.db.models import Q

import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', nargs='+', type=str)

    def myprint(self, str):
        print(datetime.datetime.now().strftime('%d.%m.%Y %H:%M') + ": " + str)

    def getWorkingBids(self):
        return Bid.objects.filter(Q(_status__exact='O') | Q(_status__exact='R'))

    def closeBids(self, bids):
        for bid in bids:
            # Время истекло поэтому меяем статус и отправляем сообщение
            if bid.timeleft == 0:
                bid.close()

    def handle(self, *args, **options):
        self.myprint("Report started")
        self.closeBids(self.getWorkingBids())
        self.myprint("Report finished")