from django.shortcuts import render

from .models import User, Bid


def profile(request):
    if request.user.is_authenticated():
        context = {}
        bids = Bid.objects.filter(author=request.user)

        context["bids"] = bids
        return render(request, 'core/profile.html')