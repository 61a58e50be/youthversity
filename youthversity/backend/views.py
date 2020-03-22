from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Subject, Post, User, CommentReply, Comment, ViolationReport
from .forms import SignUpForm, ProjectForm
from .forms import ReportForm, CommentCreationForm
import random
from itertools import chain
from django.urls import reverse
from .forms import SignUpForm
from .models import Subject, Post, User, Comment, ViolationReport

from .ownUtilities.servermail import serverStatus



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
    # get different variables used to evaluate feed
    user = request.user.be_user
    userPosts = Post.objects.filter(author=user)
    userComments = Comment.objects.filter(author=user)
    subjects = Subject.objects.all()
    likedPosts = Post.objects.order_by('-upvotes')[:2]

    # create list containing importance-values of all subjects
    values = []
    for i in range(len(subjects)):
        values.append(0)

    for post in userPosts:
        index = 0
        for i, item in enumerate(subjects):
            if item == post.subject:
                index = i
                break
        values[index] += 3

    for comment in userComments:
        index = 0
        for i, item in enumerate(subjects):
            if item == comment.parent.subject:
                index = i
                break
        values[index] += 1

    # get three most important subjects
    feedSubjects = []

    for i in range(3):
        if max(values) == 0:
            index = random.randint(0, len(subjects)-1)
            feedSubjects.append(subjects[index])
        else:
            index = values.index(max(values))
            feedSubjects.append(subjects[values.index(max(values))])
        values[index] = 0

    # select posts
    feedPosts1 = Post.objects.filter(subject=feedSubjects[0]).order_by('-created')
    if len(feedPosts1) > 4:
        feedPosts1 = feedPosts1[:4]
    feedPosts2 = Post.objects.filter(subject=feedSubjects[1]).order_by('-created')
    if len(feedPosts2) > 3:
        feedPosts2 = feedPosts2[:3]
    feedPosts3 = Post.objects.filter(subject=feedSubjects[2]).order_by('-created')
    if len(feedPosts3) > 3:
        feedPosts3 = feedPosts3[:3]

    feedPosts = list(chain(feedPosts1, feedPosts2, feedPosts3))

    # add two most liked projects if not already suggested
    for i in range(2):
        alreadyUsed = False
        print(likedPosts[i])
        for n in feedPosts:
            print(n)
            if n == likedPosts[i]:
                alreadyUsed = True
                break
    print(alreadyUsed)
    if alreadyUsed == False:
        feedPosts = list(chain(feedPosts, likedPosts))

    context = {"feedPosts" : feedPosts}
    return render(request, 'feed.html', context)


def projects_id(request, id):
    post = Post.objects.get(pk=id)
    context = {
        "Post": post,
        "Comments": Comment.objects.filter(parent=post)
        }
    return render(request, 'project.html', context)


def topics(request):
    context = {"subjects": Subject.objects.filter(parent=None)}
    return render(request, 'topics.html', context)


def subtopics(request, id):
    childs = Subject.objects.filter(parent=id)
    if not childs:
        url = reverse('projects_filter') + "?topics={}".format(id)
        return HttpResponseRedirect(url)
    context = {
        "subjects": childs,
        "parent": Subject.objects.get(pk=id),
        }
    return render(request, 'subtopics.html', context)

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
        projects=Post.objects.filter(author=request.user.be_user)
    )
    return render(request, 'projects_my.html', context)


@login_required
def projects_saved(request):
    context = dict(
        projects=request.user.be_user.saved_posts.all()
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
            msg = form.cleaned_data.get('message')
            ViolationReport(content=msg, author=request.user.be_user, done=False, flagged_type='project', content_id=id).save()
            serverStatus('New Violation report:'+msg+'for project'+str(id))
            return HttpResponse('Thanks for submitting, your report will be processed')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReportForm()

    return render(request, 'legal/report.html', {'form': form, "id": id})


@login_required
def project_new_comment(request, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = Post.objects.get(pk=id)
            text = request.POST.get('content')
            Comment.objects.create(parent=post, author=request.user.be_user, edited=False, content=text, type='comment')
            return HttpResponseRedirect('/projects/' + str(id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentCreationForm()

    return render(request, 'project_new_comment.html', {'form': form, "id": id})


@login_required
def projects_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            user = request.user.be_user
            content = form.cleaned_data.get('content')
            subject = form.cleaned_data.get('subject')
            title = form.cleaned_data.get('title')
            for s in Subject.objects.all():
                if s.name == subject:
                    subject = s
                    break
            p = Post(content=content, author=user, edited=False, type='post', subject=subject, visibility='all', title=title)
            p.save()
            return render(request, 'index.html')
    else:
        form = ProjectForm()
    context = {'form':form}
    return render(request, 'projects_new.html', context)

@login_required
def upvote_post(request, id):
    user = request.user.be_user

    try:
        curr_upvotes = Post.objects.filter(pk=id)[0].upvotes
        curr_upvotes.add(user)
    except Exception as err:
        return render(request, '404.html')

    return redirect(reverse('projects_id', kwargs={"id":id}))

@login_required
def upvote_comment(request, id):
    user = request.user.be_user

    try:
        comment = Comment.objects.filter(pk=id)[0]
        curr_upvotes = comment.upvotes
        curr_upvotes.add(user)
    except Exception as err:
        return render(request, '404.html')

    return redirect(reverse('projects_id', kwargs={"id":comment.parent.id}))


def projects_all(request):
    context = dict(posts=Post.objects.all())
    return render(request, 'projects_all.html', context=context)

def report_comment(request, id):
    def report(request, id):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ReportForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                msg = form.cleaned_data.get('message')
                ViolationReport(content=msg, author=request.user.be_user, done=False,flagged_type='comment', content_id=id).save()
                serverStatus('New Violation report:' + msg + 'for project' + str(id))
                return HttpResponse('Thanks for submitting, your report will be processed')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = ReportForm()

        return render(request, 'legal/report_comment.html', {'form': form, "id": id})
