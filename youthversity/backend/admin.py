from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Post, Feed, SchoolClass, ViolationReport, Subject, Comment, CommentReply
from .models import User as Student


# Register your models here.
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'students'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Post)
admin.site.register(Feed)
admin.site.register(SchoolClass)
admin.site.register(ViolationReport)
admin.site.register(Subject)
admin.site.register(Comment)
admin.site.register(CommentReply)

