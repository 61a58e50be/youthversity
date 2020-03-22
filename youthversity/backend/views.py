from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Subject, Post, User, CommentReply, Comment
from .forms import SignUpForm
from .forms import ReportForm, CommentCreationForm


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
    context = {}
    return render(request, 'feed.html', context)


def projects_id(request, id):
    url = request.path
    context = {"Post": Post.objects.all()[id], "Comments": Comment.objects.filter(parent=Post.objects.all()[id])}
    return render(request, 'project.html', context)


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

@login_required
def me(request):
    context = dict(
        email=request.user.email,
        username=request.user.be_user.name,
        type=request.user.be_user.type,
        language=request.user.be_user.language
    )
    return render(request, 'me.html', context)


def comment_guidelines(request):
    return render(request, 'legal/comment_guidelines.html')

def project_guidelines(request):
    return render(request, 'legal/project_guidelines.html')

def about_us(request):
    return render(request, 'about_us.html')


def copyright(request):
    return render(request, 'legal/copyright.html')

@login_required
def comments_my(request):
    context = dict(
        Comments=Comment.objects.filter(author=request.user.be_user)
    )
    return render(request, 'comments_my.html', context)

@login_required
def projects_my(request):
    context = dict(
        Projects=Post.objects.filter(author=request.user.be_user)
    )
    return render(request, 'projects_my.html', context)

@login_required
def projects_saved(request):
    context = dict(
        Projects=request.user.user_be.saved_posts
    )
    return render(request, 'projects_saved.html', context)

@login_required
def report(request, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponse('Thanks for submitting, your report will be processed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReportForm()

    return render(request, 'legal/report.html', {'form': form,"id":id})


@login_required
def project_new_comment(request, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post=Post.objects.all()[id]
            text=request.POST.get('content')
            print(text)
            Comment.objects.create(parent=post,author=request.user.be_user,edited=False,content=text,type='comment')
            return HttpResponseRedirect('/projects/'+str(id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentCreationForm()

    return render(request, 'project_new_comment.html', {'form': form, "id": id})

def profile_redirect(request):
    return HttpResponseRedirect('/me')