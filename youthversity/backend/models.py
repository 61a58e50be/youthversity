from django.db import models

# Create your models here.

class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Feed(models.Model):
    interested_in_subjects = models.CharField(max_length=10)

class User(CommonInfo):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10)
    feed = models.ForeignKey(Feed)
    language = models.CharField(max_length=2)
    saved_posts = models.ManyToManyField("Post")
    friends = models.ManyToManyField("self")

class SchoolClass(CommonInfo):
    teachers = models.ManyToManyField(User)
    students = models.ManyToManyField(User)
    school_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

class ContentBase(CommonInfo):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    edited = models.BooleanField()
    type = models.CharField(max_length=10)
    upvotes = models.ManyToManyField(User)

    class Meta:
        abstract = True

class Post(ContentBase):
    subject = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10)

class Comment(ContentBase):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)

class CommentReply(ContentBase):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE)
