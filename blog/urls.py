from django.urls import path
from blog import views


app_name = 'blog'


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:slug>/', views.post, name='post'),
    path('posts/category/', views.category, name='category'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout')
]
