from django.contrib.auth.models import User as AuthUser
from django.db import models
from .managers import PostMostUpvotesManager


# Create your models here.
class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Feed(models.Model):
    interested_in_subjects = models.CharField(max_length=10)


class User(models.Model):
    auth_user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name='be_user')
    created = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_edited = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, blank=True, null=True)
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, blank=True, null=True)
    language = models.CharField(max_length=2, blank=True, null=True)
    saved_posts = models.ManyToManyField("Post")
    friends = models.ManyToManyField("self")

    def __str__(self):
        return f"BeUser #{self.id}: '{self.name}'"


class SchoolClass(CommonInfo):
    teachers = models.ManyToManyField(
        User, related_name="school_classs_member")
    students = models.ManyToManyField(
        User, related_name="school_classs_teaching")
    school_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class ViolationReport(CommonInfo):
    flagged_type = models.TextField()
    content_id = models.PositiveIntegerField()
    content = models.TextField()
    answer = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL, related_name="violation_reports_authored")
    processor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name="violation_reports_processed")
    done = models.BooleanField()
    result = models.BooleanField(default=False)


class ContentBase(CommonInfo):
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL, related_name="%(class)s_authored")
    edited = models.BooleanField()
    type = models.CharField(max_length=10)
    upvotes = models.ManyToManyField(User)
    blocked = models.BooleanField(default=False)

    # Model managers
    objects = models.Manager()  # The default manager.
    most_popular = PostMostUpvotesManager()  # custom manager sorting by upvotes

    class Meta:
        abstract = True


class Subject(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name="childs")

    def get_parent(self):
        return self.parent if self.parent else self

    def __str__(self):
        return f"Subject #{self.id}: '{self.name}' parent '{self.parent}'"


class Post(ContentBase):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10)
    calls = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post #{self.id}: '{self.title}' by '{self.author}' in '{self.subject}'"


class Comment(ContentBase):
    parent = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="childs")

    def get_parent_post(self):
        return self.parent


class CommentReply(ContentBase):
    parent = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="childs")

    def get_parent_post(self):
        return self.parent.parent
