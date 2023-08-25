from django.urls import path
from base.views.ping_views import create_or_increment_ping, get_ping_value

urlpatterns = [
    path('inc/', create_or_increment_ping, name='create_or_increment_ping'),
    path('info/<int:dc_user>/', get_ping_value, name='get_ping_value'),
]

