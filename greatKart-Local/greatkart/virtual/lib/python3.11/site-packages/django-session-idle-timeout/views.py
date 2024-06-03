# -*- coding: UTF-8 -*-
from django.views.generic import View
from django.http import HttpResponse

class PingView(View):
    def get(self, request):
        return HttpResponse('pong')
