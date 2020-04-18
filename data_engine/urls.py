from django.urls import path
from .views import get_global_data, get_country_data, get_indian_state_data

urlpatterns = [
    path('india/', get_indian_state_data, name='get_india_state_data'),
]
