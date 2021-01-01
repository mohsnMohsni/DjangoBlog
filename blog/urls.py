from django.urls import path
from blog.views import (
    HomeView, PostView, PostsView, CategoryView,
    AddPostView, EditPostView, add_comment, like_comment, get_comments
)
from .api import post_list, comments_list

app_name = 'blog'

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('posts/', PostsView.as_view(), name='posts'),
                  path('post/<slug:slug>/', PostView.as_view(), name='post'),
                  path('category/<str:cat>/', CategoryView.as_view(), name='category'),
                  path('add_post/', AddPostView.as_view(), name='add_post'),
                  path('edit_post/<slug:slug>/', EditPostView.as_view(), name='edit_post'),
              ] + [
                  path('add_comment/', add_comment, name='add_comment'),
                  path('comment_like/', like_comment, name='like_comment'),
                  path('get_comments/<slug:slug>/', get_comments, name='comments'),
                  path('posts_api/', post_list, name='posts_api'),
                  path('comments_api/', comments_list, name='comment_api'),
              ]
