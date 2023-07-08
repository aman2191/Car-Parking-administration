from django.urls import path

from parking.views import (
    register_user,
    get_parking_spots,
    search_parking_spots,
    create_reservation,
    get_reservations
)

urlpatterns = [
    path('register', register_user, name='register'),
     path('parking-spots', get_parking_spots, name='get_parking_spots'),
    path('parking-spots/search', search_parking_spots),
    path('create-reservation', create_reservation, name='create-reservation'),
    path('reservations', get_reservations),
]
