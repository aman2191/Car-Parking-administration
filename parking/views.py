from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import geodesic
from django.shortcuts import render, redirect

from .models import ParkingSpot, Reservation, User
from .utils import calculate_price

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        user = User(email=email, phone_number=phone_number)
        user.save()
        return redirect('get_parking_spots')

    return render(request, 'register.html')

def get_parking_spots(request):
    parking_spots = ParkingSpot.objects.all()

    return render(request, 'get_parking_spots.html', {'parking_spots': parking_spots})


def search_parking_spots(request):
    if request.method == 'GET':
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))
        radius = float(request.GET.get('radius'))

        nearby_parking_spots = ParkingSpot.objects.all()
        filtered_parking_spots = []

        for parking_spot in nearby_parking_spots:
            distance = calculate_distance(latitude, longitude, parking_spot.latitude, parking_spot.longitude)
            if distance <= radius:
                filtered_parking_spots.append(parking_spot)

        return render(request, 'search_parking_spots.html', {'parking_spots': filtered_parking_spots})


from django.shortcuts import render, redirect

from django.shortcuts import render, redirect, get_object_or_404

@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        parking_spot_id = request.POST.get('parking_spot_id')
        hours = int(request.POST.get('hours'))

        user = get_object_or_404(User, pk=user_id)
        parking_spot = get_object_or_404(ParkingSpot, pk=parking_spot_id)

        total_price = calculate_price(hours)  # Implement your price calculation logic

        reservation = Reservation(user=user, parking_spot=parking_spot, hours=hours, total_price=total_price)
        reservation.save()

        return redirect('get_reservations')

    # Get the user_id and parking_spot_id from the request query parameters
    user_id = request.GET.get('user_id')
    parking_spot_id = request.GET.get('parking_spot_id')

    context = {
        'user_id': user_id,
        'parking_spot_id': parking_spot_id,
        'total_price': calculate_price(0),  # Initial price is 0, update as per your logic
        'error_message': None,  # Default value for error message
    }

    return render(request, 'create_reservation.html', context)

def get_reservations(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')

        reservations = Reservation.objects.filter(user_id=user_id)

        return render(request, 'get_reservations.html', {'reservations': reservations})

