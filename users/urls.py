from django.conf.urls import url
from django.contrib import admin
import users.views
urlpatterns = [
    url(r'^$', users.views.IndexView.as_view()),
    url(r'^status$', users.views.StatusView.as_view()),
    url(r'^see-you-later$', users.views.SeeYouView.as_view()),
    url(r'^find$', users.views.FindByTokenView.as_view(), name='submit'),
    url(r'^token/$', users.views.FindByTokenView.as_view(), name='submit'),
]
