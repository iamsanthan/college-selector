from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def TestPage(request):
    return render(request,'firstweb/test.html')

class LS(TemplateView):
    template_name='firstweb/ls.html'