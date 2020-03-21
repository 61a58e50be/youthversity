from django.shortcuts import render
from .models import Post, Comment, CommentReply


from .models import Subject
from django.http import HttpResponse


# Create your views here.
def feed(request):
    context = {}
    return render(request, 'feed.html', context)


def projects_id(request,id):
    url=request.path
    context = {"Post":Post.objects.all()[id]}

    return HttpResponse(id)#render(request,'project.html', context)


def topics(request):
    context = {"subjects": Subject.objects.all()}
    return render(request, 'topics.html', context)
