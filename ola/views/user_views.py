
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import generics

from ola.helper import user_helper

from ola.models import *
from ola.serializers.serializer import UserAccountSerializer, BankDetailSerializer, BookingHistorySerializer


class UserAccountRegistrationView(generics.CreateAPIView):
    serializer_class = UserAccountSerializer

    def change_valid_format(self, data):
        email = data.get('email')
        date_of_birth = data.get('dob')

        data['email'] = user_helper.format_email(email)
        data['date_of_birth'] = user_helper.format_dob(date_of_birth)
        return data

    def create(self, request, *agrs, **kwargs):
        serializer = self.serializer_class
        data = request.data
        data = self.change_valid_format(data)

        serialized_user = serializer(data=data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            if user:
                token = Token.objects.create(user=user)
                return Response("User account is successfully created.", status=201)

            return Response("User account not created", status=400)

        return Response(serialized_user.errors, status=400)

    def post(self, request):
        return self.create(request)


class BankDetailsView(generics.CreateAPIView):
    serializer_class = BankDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class
        data = request.data

        user = self.request.user
        data['user'] = user
        serialized_data = serializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=201)

        return Response(serialized_data.errors, status=400)

    def post(self, request):
        return self.create(request)


class GetBookingHistoryView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = BookingHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if not ((user.type == UserAccount.TYPE_DRIVER or user.type == UserAccount.TYPE_USER)
        and user.profile_status == UserAccount.STATUS_VERIFIED):
            return None

        bookings = user.bookinghistory_set.all()
        return bookings

    def list(self, request, *args, **kwargs):
        bookings = self.get_queryset()
        if not bookings:
            return Response("No bookings found.", status=200)

        serializer = self.serializer_class
        serialized_bookings = serializer(bookings, many=True)
        return Response(serialized_bookings.data, status=200)

    def get(self, request):
        return self.list(request)
