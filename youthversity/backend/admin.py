from django.contrib import admin

from .models import Post


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


admin.site.register(Post, PostAdmin)
