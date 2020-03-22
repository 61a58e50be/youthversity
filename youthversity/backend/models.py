from django.contrib.auth.models import User as AuthUser
from django.db import models


# Create your models here.

class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Feed(models.Model):
    interested_in_subjects = models.CharField(max_length=10)


class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='be_user')
    created = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_edited = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, blank=True, null=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True, null=True)
    language = models.CharField(max_length=2, blank=True, null=True)
    saved_posts = models.ManyToManyField("Post")
    friends = models.ManyToManyField("self")


class SchoolClass(CommonInfo):
    teachers = models.ManyToManyField(User, related_name="school_classs_member")
    students = models.ManyToManyField(User, related_name="school_classs_teaching")
    school_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class ViolationReport(CommonInfo):
    content = models.TextField()
    answer = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="violation_reports_authored")
    processor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name="violation_reports_processed")
    done = models.BooleanField()


class ContentBase(CommonInfo):
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="%(class)s_authored")
    edited = models.BooleanField()
    type = models.CharField(max_length=10)
    upvotes = models.ManyToManyField(User)

    class Meta:
        abstract = True


class Subject(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name="childs")



class Post(ContentBase):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10)


class Comment(ContentBase):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="childs")


class CommentReply(ContentBase):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="childs")
