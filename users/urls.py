from django.urls import path
from .views import RegisterView, LoginView, UserEventListView, LogoutView, UserListView


urlpatterns = [
    path('', UserListView.as_view(), name='register'),
    path('events/', UserEventListView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('Logout/', LogoutView.as_view(), name='register'),
]
