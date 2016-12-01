from django.shortcuts import render

def index(request):
    context = {}
    template_name = 'core/index.html'
    return render(request, template_name, context)

