from django.urls import path
from .views import SingInView, SignUpView, SignOutView, ProfileView, activate
from core.urls import router
from .api import UserViewSet

router.register(r'users', UserViewSet)

app_name = 'account'

urlpatterns = [
    path('login/', SingInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', ProfileView.as_view(), name='profile')
]
