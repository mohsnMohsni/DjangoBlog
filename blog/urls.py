from django.urls import path
from blog.views import (home, post, posts, add_post, edit_post, comment_like)


app_name = 'blog'


urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('posts/<slug:slug>/', post, name='post'),
    path('add_post/', add_post, name='add_post'),
    path('edit_post/<slug:slug>/', edit_post, name='edit_post'),
    path('comment_like/<int:cm_id>/', comment_like, name='comment_like'),
]
