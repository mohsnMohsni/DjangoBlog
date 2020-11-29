from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.posts, name='posts'),
    path('<slug:slug>/', views.post, name='post'),
    path('category/', views.category, name='category'),
]
