from django.urls import path
from .views import EventListPostView, EventDetailPutViewDelete, UserEventPostView

urlpatterns = [
    path('', EventListPostView.as_view(), name='events'),
    path('<int:event_id>/', EventDetailPutViewDelete.as_view(), name='event-detail-put'),
    path('<int:event_id>/register/', UserEventPostView.as_view(), name='user_event_registration'),
]

