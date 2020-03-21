from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def feed(request):
    context = {}
    return render(request, 'feed.html', context)


@login_required
def help(request):
    return HttpResponse("here is some help :)")
