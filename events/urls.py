from django.urls import path
from .views import EventListPostView, EventDetailPutView


urlpatterns = [
    path('', EventListPostView.as_view(), name='events'),
    path('<int:event_id>/', EventDetailPutView.as_view(), name='event-detail-put'),
]
