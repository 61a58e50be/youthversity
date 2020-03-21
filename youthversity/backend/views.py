from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Subject, Post, User
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            print(username)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(user)
            login(request, user)

            return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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


def imprint(request):
    return render(request, 'imprint.html')
