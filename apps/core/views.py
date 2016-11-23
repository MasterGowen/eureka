from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from django.db import IntegrityError

from .models import User, Bid, Answer

@require_http_methods(["GET", ])
@login_required
def profile(request):
    context = {}
    bids = Bid.objects.filter(author=request.user)

    context["bids"] = bids
    return render(request, 'core/profile.html', context)


@require_http_methods(["GET", ])
@login_required
def top_bids(request):
    context = {}
    answers = Answer.objects.all()  # TODO: filter! + commercials
    context['answers'] = answers
    return render(request, "core/top.html", context)


@require_http_methods(["GET", ])
@login_required
def bids(request):
    bids = Bid.objects.all()
    return render(request, "core/bids.html", {"bids": bids})


class BidCreate(CreateView):
    model = Bid
    fields = ['product', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BidCreate, self).form_valid(form)


class AnswerCreate(CreateView):
    model = Answer
    fields = ['description', 'price', 'currency', 'url']

    def get_success_url(self):
        return reverse('bid_detail', args=(self.object.bid.id,))

    def form_valid(self, form):
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        author = self.request.user
        if author != bid.author:
            form.instance.author = author
            form.instance.bid = bid
        try:
            return super(AnswerCreate, self).form_valid(form)
        except IntegrityError:
            form.add_error('description',  'Вы не можете отвечать на собственную заявку')
            return self.form_invalid(form)


@require_http_methods(["GET", ])
@login_required
def bid_detail(request, pk):
    bid = Bid.objects.get(pk=pk)
    answers = Answer.objects.filter(bid=bid.id)

    return render(request, "core/bid_detail.html", {"bid": bid,
                                                    "answers": answers})