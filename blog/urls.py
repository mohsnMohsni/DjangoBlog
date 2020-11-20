from django.urls import path
from blog import views


app_name = 'blog'
urlpatterns = [
    path('', views.home, name='index'),
    path('category/', views.category, name='category'),
    path('<slug:slug>/', views.single, name='single'),
]
