from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .models import Subject, Post, User, Comment, CommentReply
from .forms import SignUpForm
import random


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            auth_user = form.save(commit=False)
            auth_user.save()

            username = form.cleaned_data.get('username')
            if not username:
                raise HttpResponseBadRequest('Username empty.')
            print(username)
            #auth_user.be_user = User(name=username)
            be_user = User(name=username, auth_user=auth_user)
            be_user.save()

            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # print(user)
            login(request, auth_user)

            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Create your views here.
@login_required
def index(request):
    context = dict(user=request.user.be_user)
    return render(request, 'index.html', context=context)


@login_required
def feed(request):
    # get different variables used to evaluate feed
    user = request.user.be_user
    userPosts = Post.objects.filter(author=user)
    userComments = Comment.objects.filter(author=user)
    subjects = Subject.objects.all()

    # create list containing importance-values of all subjects
    values = []
    for i in range(len(subjects)):
        values.append(0)

    for post in userPosts:
        values[subjects.index(post.subject)] += 3

    for comment in userComments:
        values[subjects.index(comment.parent.subject)] += 1

    # get three most important subjects
    feedSubjects = []

    if max(values) == 0:
        randNums = random.sample(range(0, len(subjects)), 3)
        for n in randNums:
            feedSubjects.append(subjects[n])

    else:
        for i in range(3):
            feedSubjects.append(subjects[values.index(max(values))])
            values[values.index(max(values))] = 0

    # select posts
    feedPosts1 = Post.objects.order_by('-created')[4]
    feedPosts2 = Post.objects.order_by('-created')[3]
    feedPosts3 = Post.objects.order_by('-created')[3]
    feedPosts = feedPosts1 + feedPosts2 + feedPosts3

    context = {feedPosts : feedPosts}
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
