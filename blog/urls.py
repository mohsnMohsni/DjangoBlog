from django.urls import path, include
from blog.views import (
    HomeView, PostView, PostsView, CategoryView,
    AddPostView, EditPostView, add_comment, like_comment, get_comments
)
from .api import (post_list, post_detail, comments_list, PostList, PostDetail,
                  PostListMixin, PostDetailMixin, PostListGeneric, PostDetailGeneric,
                  PostViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

post_router = router.register(r'router_post', PostViewSet)

post_viewset = PostViewSet.as_view({"get": "list",
                                           "post": "create",
                                           "put": "update",
                                           "delete": "destroy"})

app_name = 'blog'

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('posts/', PostsView.as_view(), name='posts'),
                  path('post/<slug:slug>/', PostView.as_view(), name='post'),
                  path('category/<str:cat>/', CategoryView.as_view(), name='category'),
                  path('add_post/', AddPostView.as_view(), name='add_post'),
                  path('edit_post/<slug:slug>/', EditPostView.as_view(), name='edit_post'),
                  path('add_comment/', add_comment, name='add_comment'),
                  path('comment_like/', like_comment, name='like_comment'),
                  path('get_comments/<slug:slug>/', get_comments, name='comments'),
              ] + [
                  path('post_list/', post_list, name='post_list'),
                  path('comments_list/', comments_list, name='comment_list'),
                  path('post_detail/<int:pk>/', post_detail, name='post_detail'),
                  path('class_postlist/', PostList.as_view(), name='class_postlist'),
                  path('class_postdetail/<int:pk>/', PostDetail.as_view(),
                       name='class_postdetail'),
                  path('mixin_postlist/', PostListMixin.as_view(), name='mixin_postlist'),
                  path('mixin_postdetail/<int:pk>/', PostDetailMixin.as_view(),
                       name='mixin_postdetail'),
                  path('generic_postlist/', PostListGeneric.as_view(), name='generic_postlist'),
                  path('generic_postdetail/<int:pk>/', PostDetailGeneric.as_view(),
                       name='generic_postdetail'),
                  path('modelview_post/', post_viewset, name='modelview_post'),
                  path('router/', include(router.urls)),
              ]
