from django.shortcuts import render
import subprocess
from django.template import RequestContext


def last_date_processor(request):
    cmd = "git show -s --format=%ci"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print "output: ", output
    print "error: ", error
    return {'last_revision_date': output}


def index(request):
    context = RequestContext(request, {}, [last_date_processor])
    template_name = 'core/index.html'
    print "from index view: last_revision_date: ", context
    return render(request, template_name, context)
