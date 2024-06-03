# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r"^/?", views.PingView.as_view(), name="django-session-idle-timeout_ping"),
)
