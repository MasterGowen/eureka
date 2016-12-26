from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.core import serializers

from django.db import IntegrityError

from .models import User, Bid, Answer
from .forms import BidForm
from apps.core.management.commands.report import Command

@require_http_methods(["GET", ])
@login_required
def test(request):
    context = {}
    bids = Command.getWorkingBids({})
    context["testObj"] = bids
    Command.closeBids({}, bids)
    return render(request, 'core/test.html', context)

@require_http_methods(["GET", ])
@login_required
def profile(request):
    context = {}
    bids = Bid.objects.filter(author=request.user)


    context["bids"] = bids
    return render(request, 'core/profile.html', context)

@require_http_methods(["GET", ])
def home(request):
    context = {}
    return render(request, "core/home.html", context)

@require_http_methods(["GET", ])
@login_required
def top_bids(request):
    context = {}

    bids = Bid.objects.filter(status__exact='C')
    answers = []

    for bid in bids:
        try:
            answers.append(Answer.objects.filter(bid=bid.id).order_by('price')[0])
        except:
            pass

    context['answers'] = answers
    return render(request, "core/top.html", context)


@require_http_methods(["GET", ])
def bids(request):
    context = {}
    #### TOP ####
    bids = Bid.objects.filter(_status__exact='C')
    top_answers = []
    for bid in bids:
        try:
            top_answers.append(Answer.objects.filter(bid=bid.id).order_by('price')[0])
        except:
            pass
    context['top_answers'] = top_answers

    #### ALL_BIDS ####
    bids = Bid.objects.all()
    context["bids"] = bids

    #### SEARCH ####!
    from haystack.forms import SearchForm
    form = SearchForm(request.GET)
    query = form.search()

    try:
        if request.GET["q"]:
            context["is_search"] = True
    except:
        pass

    context["form"] = form
    context["query"] = query

    bid_form = bid_create(request, True)
    #if request.method == "POST"
    context["bid_form"] = bid_form

    return render(request, "core/bids.html", context)



@csrf_protect
def bid_create(request, get_form=False):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            try:
                bid.author = request.user
            except:
                pass
            bid.save()
            return redirect(bid)
    context = {}
    context['form'] = BidForm()
    if get_form is True:
        return BidForm()
    return render(request, 'core/bid_form.html', context)



class AnswerCreate(CreateView):
    model = Answer
    fields = ['description', 'price', 'currency', 'url']

    def get_success_url(self):
        return reverse('bid_detail', args=(self.object.bid.id,))

    def form_valid(self, form):
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        author = self.request.user
        try:
            if author != bid.author:
                form.instance.author = author
                form.instance.bid = bid
        except:
            form.instance.author = author
            form.instance.bid = bid
        try:
            return super(AnswerCreate, self).form_valid(form)
        except IntegrityError:
            form.non_field_errors('Вы не можете отвечать на собственную заявку')
            return self.form_invalid(form)


@require_http_methods(["GET", ])
def bid_detail(request, pk):
    bid = Bid.objects.get(pk=pk)
    answers = Answer.objects.filter(bid=bid.id)

    return render(request, "core/bid_detail.html", {"bid": bid,
                                                    "answers": answers})

@require_http_methods(["GET", ])
@login_required
def answers(request, pk):
    bid = Bid.objects.get(pk=pk)
    answers = Answer.objects.filter(bid=bid.id)
    data_json = {
        'bid': serializers.serialize('json', [bid]),
        'answers': serializers.serialize('json', list(answers)),
    }
    return JsonResponse(data_json)