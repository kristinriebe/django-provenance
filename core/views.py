from django.shortcuts import render
from django.template import RequestContext

def index(request):
    context = {}
    template_name = 'core/index.html'
    return render(request, template_name, context)
