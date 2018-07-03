from django.db import transaction
from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes

from ola.builder.response_builder import ResponseBuilder
from ola.entity.booking_history import UserBookingHistory
from ola.entity.cabs import Cabs
from ola.entity.customer import CustomerProfile
from ola.models import BookingHistory


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def api_check_all_available_cabs(request):
    response_builder = ResponseBuilder()
    data = request.GET

    latitude = data.get('x', 0.0)
    longitude = data.get('y', 0.0)
    radius = data.get('radius', 3000)

    if not (latitude and longitude and radius):
        return response_builder.ok_200().failure().message("Please provide your location").get_response()

    cab = Cabs()
    status, message, nearby_cabs = cab.get_nearby_available_cabs(latitude, longitude, radius)
    if not status:
        return response_builder.ok_200().failure().message("No cabs available nearby").get_response()

    result = dict(cabs=nearby_cabs)
    return response_builder.ok_200().success().message("Some cabs are available nearby").response_data(result).get_response()


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def api_get_all_available_cabs(request):
    response_builder = ResponseBuilder()

    status, message, serialized_cabs = Cabs.get_all_serialized_cabs()
    if not status:
        return response_builder.ok_200().failure().message(message).get_response()

    return response_builder.ok_200().success().response_data({'cabs': serialized_cabs}).message(message).get_response()


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def api_book_cab(request):
    response_builder = ResponseBuilder()
    post_data = request.data

    cab_type = post_data.get('type', None)
    starting_point = post_data.get('starting', None)
    ending_point = post_data.get('ending', None)
    driver_email = post_data.get('driver', None)
    status = post_data.get('status', None)

    if not (cab_type and starting_point and ending_point and driver_email and status):
        return response_builder.ok_200().failure().message("Please provide all the details").get_response()

    if status in [BookingHistory.STATUS_BOOKED, BookingHistory.STATUS_RIDING]:
        return response_builder.ok_200().failure().message("Cab already booked").get_response()

    user = request.user
    customer = CustomerProfile(email=driver_email)
    driver = customer.get_customer_via_email()
    if not driver:
        return response_builder.ok_200().failure().message("Driver details not valid").get_response()

    with transaction.atomic():
        status, message, cabs = Cabs.check_all_available_cabs()
        cab = cabs[0]
        cab.available = False
        cab.save()

        booking = UserBookingHistory(user).create_booking(driver, starting_point, ending_point, cab)
        booking.status = BookingHistory.STATUS_BOOKED
        booking.save()

    cab = Cabs.get_serialized_cab(cab)
    return response_builder.ok_200().success().response_data({'cab': cab}).get_response()

