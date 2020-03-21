from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('feed/', views.feed, name='feed'),
    # path('topics/', views.topics, name='topics'),
    # path('projects/all/', views.projects_all, name='projects_all'),
    # path('projects/my/', views.projects_my, name='projects_my'),
    # path('projects/new/', views.projects_new, name='projects_new'),
    # path('projects/<int: id>/', views.projects_id, name='projects_id'),
    # path('projects/<int: id>/new_comment', views.project_new_comment, name='project_new_comment'),
    # path('projects/saved/', views.projects_saved, name='projects_saved'),
    # path('comments/my/', views.comments_my, name='comments_my'),
    # path('help/', views.help, name='help'),
    # path('imprint/', views.imprint, name='imprint'),
    # path('me/', views.me, name='me'),
]
