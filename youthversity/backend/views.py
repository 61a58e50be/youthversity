from django.shortcuts import render

from .models import Subject


# Create your views here.
def feed(request):
    context = {}
    return render(request, 'feed.html', context)


def topics(request):
    context = {"subjects": list([s.name for s in Subject.objects.all()])}
    return render(request, 'topics.html', context)
