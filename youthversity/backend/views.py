from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Comment, CommentReply


from .models import Subject, Post
from django.http import HttpResponse


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


def projects_id(request,id):
    url=request.path
    context = {"Post":Post.objects.all()[id],"Comments":Comment.object.filter(parent=Post.objects.all()[id])}
    return render(request,'project.html', context)


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


def imprint(request):
    return render(request, 'legal/imprint.html')

def privacy(request):
    return render(request, 'legal/privacy.html')

def faq(request):
    return render(request, 'faq.html')
