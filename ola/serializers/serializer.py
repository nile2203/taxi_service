import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from ola.models import *
from ola.helper import datetime_helper


class RatingBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['stars', 'comment']


class BookingHistorySerializer(serializers.ModelSerializer):
    rating = RatingBasicSerializer()
    booking_id = serializers.SerializerMethodField()
    date_of_booking = serializers.SerializerMethodField()

    def get_date_of_booking(self, booking):
        if booking.date_of_booking:
            return datetime_helper.get_user_readable_date(booking.date_of_booking)
        return " "

    def get_booking_id(self, booking):
        return booking.booking_id[:8]

    @staticmethod
    def get_serialized(booking, many=False):
        history = BookingHistorySerializer(booking, many=many).data
        return json.loads(JSONRenderer().render(history))

    class Meta:
        model = BookingHistory
        fields = ['booking_id', 'fare', 'date_of_booking', 'starting_point', 'ending_point',
                    'status', 'rating']


class CabSerializer(serializers.ModelSerializer):

    @staticmethod
    def get_serialized(cabs, many=False):
        data = CabSerializer(cabs, many=many).data
        return json.loads(JSONRenderer().render(data))

    class Meta:
        model = Cab
        exclude = ('created', 'modified', 'location')
