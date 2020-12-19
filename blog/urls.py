from django.urls import path
from blog.views import (
    HomeView, PostView, PostsView, AddPostView, EditPostView, CommentLikeView
)


app_name = 'blog'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('post/<slug:slug>/', PostView.as_view(), name='post'),
] + [
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('edit_post/<slug:slug>/', EditPostView.as_view(), name='edit_post'),
    path('comment_like/<int:cm_id>/', CommentLikeView.as_view(), name='comment_like'),
]
