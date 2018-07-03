from ola.helper.datetime_helper import get_current_date
from ola.models import BookingHistory
from ola.serializers.serializer import BookingHistorySerializer


class UserBookingHistory:
    def __init__(self, user=None):
        self.user = user

    def get_all_bookings(self):
        bookings = self.user.bookinghistory_set.all()
        return bookings

    def get_all_serialized_bookings(self):
        bookings = self.get_all_bookings()
        if not bookings:
            return 0, "No bookings yet", None

        serialized_bookings = BookingHistorySerializer.get_serialized(bookings, many=True)
        return 1, "", serialized_bookings

    def create_booking(self, driver, starting_point, ending_point, cab):
        booking = BookingHistory.objects.create(fare=100.0,
                                                driver=driver,
                                                user=self.user,
                                                starting_point=starting_point,
                                                ending_point=ending_point,
                                                date_of_booking=get_current_date(),
                                                cab=cab)
        return booking
