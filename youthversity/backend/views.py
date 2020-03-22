from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Subject, Post, Comment, CommentReply
from django.http import HttpResponse
from .forms import ReportForm


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


def projects_id(request, id):
    url = request.path
    context = {"Post": Post.objects.all()[id], "Comments": Comment.object.filter(parent=Post.objects.all()[id])}
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


def me(request):
    context = dict(
        email=request.user.email,
        username=request.user.be_user.name,
        type=request.user.be_user.type,
        language=request.user.user_be.language
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
        Comments=Comment.objects().filter(author=request.user.user_be)
    )
    return render(request, 'comments_my.html', context)


def projects_my(request):
    context = dict(
        Projects=Post.objects().filter(author=request.user.user_be)
    )
    return render(request, 'projects_my.html', context)


def projects_saved(request):
    context = dict(
        Projects=request.user.user_be.saved_posts
    )
    return render(request, 'projects_saved.html', context)


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
