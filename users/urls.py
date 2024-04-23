from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('Logout/', LogoutView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='register'),
]
