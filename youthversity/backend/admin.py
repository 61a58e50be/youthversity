from django.contrib import admin

from .models import Post, User


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ["subject",
              "title",
              "visibility",
              "content",
              "author",
              "edited",
              "type",
              "upvotes",
              ]


class UserAdmin(admin.ModelAdmin):
    fields = [
        "auth_user",
        "name",
        "type",
        "feed",
        "language",
        "saved_posts",
        "friends"
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
