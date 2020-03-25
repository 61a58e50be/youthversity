from django.db import models
from django.db.models import Count


class PostMostUpvotesManager(models.Manager):
    """
    returns the posts ordered by upvotes. index 0 has the most.
    """

    def get_queryset(self):
        return super(PostMostUpvotesManager, self).get_queryset(). \
            annotate(upvote_count=Count('upvotes')).order_by('-upvote_count')
