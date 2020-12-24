from django.urls import path
from blog.views import (
    HomeView, PostView, PostsView, CategoryView,
    AddPostView, EditPostView, AddCommentView, like_comment, get_comment
)

app_name = 'blog'

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('posts/', PostsView.as_view(), name='posts'),
                  path('post/<slug:slug>/', PostView.as_view(), name='post'),
                  path('category/<str:cat>/', CategoryView.as_view(), name='category'),
                  path('get_commnets/', get_comment, name='comments'),
              ] + [
                  path('add_post/', AddPostView.as_view(), name='add_post'),
                  path('edit_post/<slug:slug>/', EditPostView.as_view(), name='edit_post'),
                  path('add_comment/<slug:slug>/', AddCommentView.as_view(), name='add_comment'),
                  path('comment_like/', like_comment, name='like_comment'),
              ]
