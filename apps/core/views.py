from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import User, Bid, Answer

@require_http_methods(["GET", ])
@login_required
def profile(request):
    context = {}
    bids = Bid.objects.filter(author=request.user)

    context["bids"] = bids
    return render(request, 'core/profile.html')


@require_http_methods(["GET", ])
@login_required
def top_bids(request):
    context = {}
    answers = Answer.objects.all()  # TODO: filter! + commercials
    context['answers'] = answers
    return render(request, "core/top.html", context)

