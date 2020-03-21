from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import Subject, Post


# Create your views here.
@login_required
def index(request):
    user = request.user.id
    context = dict(user=user)
    return render(request, 'index.html', context=context)


@login_required
def feed(request):
    context = {}
    return render(request, 'feed.html', context)


@login_required
def topics(request):
    context = {"subjects": Subject.objects.all()}
    return render(request, 'topics.html', context)


@login_required
def projects_filter(request):
    if request.method != 'GET':
        # Todo: implement an error page
        return HttpResponse('400 - Bad Request')

    topics = request.GET.get('topics')

    if topics:
        filtered = Post.objects.filter(pk__in=topics)
        context = dict(
            posts=filtered,
            query=list(request.GET.items())
        )
        return render(request, 'projects_filter.html', context)

    return HttpResponse('400 - Bad Request')
