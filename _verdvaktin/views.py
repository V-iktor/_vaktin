import re
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from _verdvaktin.models import Cpu

class IndexView(generic.ListView):
    template_name = "_verdvaktin/index.html"
    context_object_name = "cpus"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Cpu.objects.all()

def save(request, cpu_id):
    value=request.POST.get('regex')
    try:
        re.compile(value)
 
    except re.error:
        return HttpResponseRedirect("/?invalid-regex")
    
    cpu = get_object_or_404(Cpu, pk=cpu_id)
    cpu.regex = value
    cpu.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect("/")
