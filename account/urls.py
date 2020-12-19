from django.urls import path
from .views import SingInView, SignUpView, SignOutView

app_name = 'account'

urlpatterns = [
    path('login/', SingInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register')
]
