from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import Subject, Post, User, Comment


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            auth_user = form.save(commit=False)
            auth_user.save()

            username = form.cleaned_data.get('username')
            if not username:
                raise HttpResponseBadRequest('Username empty.')

            be_user = User(name=username, auth_user=auth_user)
            be_user.save()
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
    context = {}
    return render(request, 'feed.html', context)


def projects_id(request, id):
    context = {"Post": Post.objects.all()[id], "Comments": Comment.objects.filter(parent=Post.objects.all()[id])}
    return render(request, 'project.html', context)


@login_required
def topics(request):
    context = {"subjects": Subject.objects.filter(parent=None)}
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


def me(request):
    context = dict(
        email=request.user.email,
        username=request.user.be_user.name,
        type=request.user.be_user.type,
        language=request.user.be_user.language
    )
    return render(request, 'me.html', context)


def rules(request):
    return render(request, 'legal/rules.html')


def about_us(request):
    return render(request, 'about_us.html')


def copyright(request):
    return render(request, 'legal/copyright.html')


def comments_my(request):
    context = dict(
        comments=Comment.objects.filter(author=request.user.be_user)
    )
    return render(request, 'comments_my.html', context)


def projects_my(request):
    context = dict(
        projects=Post.objects.filter(author=request.user.be_user)
    )
    return render(request, 'projects_my.html', context)


def projects_saved(request):
    context = dict(
        projects=request.user.be_user.saved_posts.all()
    )
    return render(request, 'projects_saved.html', context)
