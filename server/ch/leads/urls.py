from django.urls import path
from .views import *


app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view() , name='lead-detail'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('update/<int:pk>/', LeadUpdateView.as_view(), name='lead-update'),
    path('delete/<int:pk>/', LeadDeleteView.as_view(), name='lead-delete'),
]