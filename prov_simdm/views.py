from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the prov_simdm index. This part of the webapp is not ready, yet.")

