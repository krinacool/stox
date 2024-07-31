from django.urls import path
from .views import *

urlpatterns = [
    path('api/token/', token_obtain_pair_view, name='token_obtain_pair'),
    path('api/place_order/', place_order, name='place_order'),
    path('api/positions/', get_positions, name='get_positions'),
    path('api/holdings/', get_holdings, name='get_holdings'),
    path('api/documentation/', documentation, name='documentation'),
    # Other API endpoints
]
