from django.urls import path
from blog.views.views import (home, post, posts, category)
from blog.views.user_auth import (log_out, log_in, register)


app_name = 'blog'


urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('posts/<slug:slug>/', post, name='post'),
    path('posts/category/', category, name='category'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register, name='register')
]
