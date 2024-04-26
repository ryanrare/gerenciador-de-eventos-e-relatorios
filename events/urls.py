from django.urls import path
from .views import EventListPostView, EventDetailPutDeleteView, UserEventPostView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Sua API de Eventos",
        default_version='v1',
        description="Uma descrição da sua API de eventos.",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('', EventListPostView.as_view(), name='events'),
    path('<int:event_id>/', EventDetailPutDeleteView.as_view(), name='event-detail-put'),
    path('<int:event_id>/register/', UserEventPostView.as_view(), name='user_event_registration'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
