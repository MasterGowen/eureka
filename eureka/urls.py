"""eureka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from apps.core.views import profile, top_bids, BidCreate, AnswerCreate, bids, bid_detail

urlpatterns = [
    #url(r'^/', include('core.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^top/$', top_bids, name="top"),
    url(r'^$', profile, name="home"),
    url(r'^bid/create/$', login_required(BidCreate.as_view()), name="bid_create"),
    url(r'^answer/create/(?P<pk>[0-9A-Za-z-]+)/$', login_required(AnswerCreate.as_view()), name="answer_create"),
    url(r'^bids/$', bids, name="bids"),
    url(r'^bid/(?P<pk>[0-9A-Za-z-]+)/$', bid_detail, name="bid_detail"),

]