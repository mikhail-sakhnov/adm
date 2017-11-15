from django.conf.urls import url
from django.contrib import admin
import users.views
urlpatterns = [
    url(r'^$', users.views.IndexView.as_view()),
    url(r'^status$', users.views.StatusView.as_view()),
    url(r'^see-you-later/(?P<token>[-\w]+)$',
        users.views.SeeYouView.as_view()),
    url(r'^find$', users.views.FindByTokenView.as_view(), name='search'),
    url(r'^token/(?P<slug>[-\w]+)/$',
        users.views.TokenControlView.as_view(), name='control'),
]
