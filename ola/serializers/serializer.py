
from rest_framework import serializers
from rest_framework.response import Response

from ola.helper.datetime_helper import get_current_date
from ola.models import *
from ola.helper import datetime_helper
from ola.validation import bank_details_validation


class RatingBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['stars', 'comment']


class BookingHistorySerializer(serializers.ModelSerializer):
    rating = RatingBasicSerializer()
    booking_id = serializers.SerializerMethodField()
    date_of_booking = serializers.SerializerMethodField()

    def create(self, **validated_data):
        cab = validated_data.get('cab')
        booking = BookingHistory.objects.create(fare=100.0,
                                                driver=cab.driver,
                                                user=validated_data.get('user'),
                                                starting_point=validated_data.get('starting_point'),
                                                ending_point=validated_data.get('ending_point'),
                                                date_of_booking=get_current_date(),
                                                cab=cab)

        cab.status = Cab.STATUS_BOOKED
        cab.save()
        return booking

    def get_date_of_booking(self, booking):
        if booking.date_of_booking:
            return datetime_helper.get_user_readable_date(booking.date_of_booking)
        return " "

    def get_booking_id(self, booking):
        return booking.booking_id[:8]

    class Meta:
        model = BookingHistory
        fields = ['booking_id', 'fare', 'date_of_booking', 'starting_point', 'ending_point',
                    'status', 'rating']


class CabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cab
        exclude = ('created', 'modified', 'location')


class UserAccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = UserAccount.objects.create_user(**validated_data)
        if user.type == UserAccount.TYPE_USER:
            user.profile_status = UserAccount.STATUS_VERIFIED
            user.save()

        elif user.type == UserAccount.TYPE_DRIVER:
            user.profile_status = UserAccount.STATUS_PENDING
            user.save()

        return user

    class Meta:
        model = UserAccount
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'type', 'profile_status')


class DriverDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverDocument
        fields = '__all__'


class BankDetailSerializer(serializers.ModelSerializer):

    @staticmethod
    def upload_document(document):
        return True

    def create(self, **validated_data):
        user = validated_data.get('user')
        proof_type = validated_data.get('proof_type')
        if user.profile_status != UserAccount.STATUS_PROCESSING:
            return Response("User is not registered with given credentials", status=400)

        if proof_type not in [DriverDocument.CHEQUE, DriverDocument.PASSBOOK]:
            return Response("Bank proofs are not valid.", status=400)

        status, message = bank_details_validation.validate_bank_information(**validated_data)
        if not status:
            return Response("Provided details are invalid", status=400)

        details = BankDetail.objects.create(bank_name=validated_data.get('bank'),
                                            account_number=validated_data.get('account'),
                                            branch_name=validated_data.get('branch'),
                                            ifsc_code=validated_data.get('ifsc'),
                                            micr_code=validated_data.get('micr'),
                                            city=validated_data.get('city'),
                                            state=validated_data.get('state'))

        proof = DriverDocument.objects.create(docuemnt_type=proof_type, description=proof_type.lower())
        document_url = BankDetailSerializer.upload_document(validated_data.get('proof'))
        proof.document_url = document_url
        proof.save()

        return details

    class Meta:
        model = BankDetail
        fields = '__all__'
