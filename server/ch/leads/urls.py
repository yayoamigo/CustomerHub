from django.urls import path
from .views import (
    lead_list,
    lead_detail,
    lead_create,
)

urlpatterns = [
    path('leads/', lead_list),
    path('leads/<int:pk>/', lead_detail),
    path('create/', lead_create),
]