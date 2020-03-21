from django.shortcuts import render
from youthversity.backend.models import Post, Comment, CommentReply
# Create your views here.
def feed(request):
    context = {}
    return render(request, 'feed.html', context)

def projects_id(request):
    url=request.path
    id=url.rsplit('/',1)[-1]
