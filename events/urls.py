from django.urls import path
from .views import EventListPostView


urlpatterns = [
    path('', EventListPostView.as_view(), name='register'),
]
