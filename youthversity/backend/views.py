from django.http import HttpResponse
from django.shortcuts import render

from .models import Subject, Post


# Create your views here.
def feed(request):
    context = {}
    return render(request, 'feed.html', context)


def topics(request):
    context = {"subjects": Subject.objects.all()}
    return render(request, 'topics.html', context)


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
