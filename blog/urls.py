from django.urls import path
from blog.views.views import (home, post, posts, category)


app_name = 'blog'


urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('posts/<slug:slug>/', post, name='post'),
    path('posts/category/', category, name='category'),
]
