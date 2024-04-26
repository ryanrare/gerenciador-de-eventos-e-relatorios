from django.urls import path
from .views import RegisterView, LoginView, UserEventListView, LogoutView, UserListView, UserNotificationsListDeleteView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('', UserListView.as_view(), name='register'),
    path('events/', UserEventListView.as_view(), name='register'),
    path('notifications/', UserNotificationsListDeleteView.as_view()),
    path('notifications/<int:notification_id>/', UserNotificationsListDeleteView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('Logout/', LogoutView.as_view(), name='register'),
]
