from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes

from ola.entity.bank_details import DriverBankDetails
from ola.entity.booking_history import UserBookingHistory
from ola.entity.driver_documents import DriverDocuments
from ola.helper import user_helper
from ola.builder.response_builder import ResponseBuilder

from ola.models import *
from ola.entity.customer import CustomerProfile
from ola.models import UserAccount
from ola.validation import bank_details_validation


@api_view(['POST'])
def api_user_registration(request):
    response_builder = ResponseBuilder()
    post_data = request.data

    email = post_data.get('email', None)
    password = post_data.get('password', None)
    phone_number = post_data.get('phone', None)
    first_name = post_data.get('first_name', None)
    last_name = post_data.get('last_name', None)
    gender = post_data.get('gender', None)
    date_of_birth = post_data.get('dob', None)
    isd_code = post_data.get('isd', None)
    type = post_data.get('type', None)

    if not (email and password and phone_number and first_name and gender and date_of_birth and type):
        return response_builder.ok_200().failure().message("Please provide all the details").get_response()

    email = user_helper.format_email(email)
    date_of_birth = user_helper.format_dob(date_of_birth)

    customer_profile = CustomerProfile(email=email, phone_number=phone_number)
    status, message = customer_profile.check_customer_exists()
    if not status:
        return response_builder.ok_200().failure().message(message).get_response()

    customer = customer_profile.create_customer_profile(password=password,
                                                        first_name=first_name,
                                                        gender=gender,
                                                        dob=date_of_birth,
                                                        last_name=last_name,
                                                        isd=isd_code)
    token = Token.objects.create(user=customer)

    if type == UserAccount.TYPE_USER:
        customer.profile_status = UserAccount.STATUS_VERIFIED
        customer.save()
    elif type == UserAccount.TYPE_DRIVER:
        customer.profile_status = UserAccount.STATUS_PENDING
        customer.save()

    return response_builder.ok_200().success().message("Registration sucsessfull").get_response()


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def api_upload_driver_documents(request):
    response_builder = ResponseBuilder()
    post_data = request.data

    email = post_data.get('email', None)
    licence = post_data.get('licence', None)
    permit = post_data.get('permit', None)
    pan = post_data.get('pan', None)
    rc = post_data.get('rc', None)
    insurance = post_data.get('insurance', None)

    if not (email and licence and permit and pan and rc and insurance):
        return response_builder.ok_200().failure().message("Please provide all the documents").get_response()

    customer = CustomerProfile(email=email)
    driver = customer.get_customer_via_email()
    if not driver:
        return response_builder.ok_200().failure().message("Email is invalid").get_response()

    if driver.profile_status != UserAccount.STATUS_PENDING:
        return response_builder.ok_200().failure().message("Please register to upload documents").get_response()

    documents = [licence, permit, pan, rc, insurance]
    driver_documents = DriverDocuments(driver)
    status, message = driver_documents.upload_driver_documents(documents)
    if not status:
        return response_builder.ok_200().failure().message(message).get_response()

    return response_builder.ok_200().success().message(message).get_response()


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def api_register_driver_bank_details(request):
    response_builder = ResponseBuilder()
    post_data = request.data

    email = post_data.get('email', None)
    bank_name = post_data.get('bank', None)
    account_number = post_data.get('account', None)
    ifsc = post_data.get('ifsc', None)
    branch_name = post_data.get('branch', None)
    micr = post_data.get('micr', None)
    city = post_data.get('city', None)
    state = post_data.get('state', None)
    proof_type = post_data.get('proof_type', None)
    bank_proof = post_data.get('proof', None)

    for value in [email, bank_name, account_number, ifsc, branch_name, micr, city, state, bank_proof, proof_type]:
        if not value:
            return response_builder.ok_200().failure().message("Please provide all the documents").get_response()

    customer = CustomerProfile(email=email)
    driver = customer.get_customer_via_email()
    if not driver:
        return response_builder.ok_200().failure().message("Email is invalid").get_response()

    if driver.profile_status != UserAccount.STATUS_PROCESSING:
        return response_builder.ok_200().failure().message("Please register and upload vehicle documents").get_response()

    if proof_type not in [DriverDocument.CHEQUE, DriverDocument.PASSBOOK]:
        return response_builder.ok_200().failure().message("Proof type is invalid").get_response()

    status, message = bank_details_validation.validate_bank_information(post_data)
    if not status:
        return response_builder.ok_200().failure().message(message).get_response()

    bank_details = DriverBankDetails.create_bank_details(post_data)
    document = DriverDocuments(type=proof_type)
    document.upload_bank_proof(bank_proof)

    return response_builder.ok_200().success().response_data().message("Driver bank details updated. Awaiting confirmation").get_response()


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def api_get_booking_history(request):
    response_builder = ResponseBuilder()
    data = request.GET

    email = data.get('email', None)
    user_type = data.get('type', None)

    if not (email and user_type):
        return response_builder.ok_200().failure().message("Please provide all the details").get_response()

    if user_type not in [UserAccount.TYPE_USER, UserAccount.TYPE_DRIVER]:
        return response_builder.ok_200().failure().message("user type is invalid").get_response()

    customer_profile = CustomerProfile(email=email)
    user = customer_profile.get_customer_via_email()
    if not user:
        return response_builder.ok_200().failure().message("Email is invalid").get_response()

    if not (user.type == UserAccount.TYPE_USER and user.profile_status == UserAccount.STATUS_VERIFIED):
        return response_builder.ok_200().failure().message("Profile registration is not completed").get_response()

    if not (user.type == UserAccount.TYPE_DRIVER and user.profile_status == UserAccount.STATUS_VERIFIED):
        return response_builder.ok_200().failure().message("Profile registration is not completed").get_response()

    booking_history = UserBookingHistory(user)
    status, message, serialized_bookings = booking_history.get_all_serialized_bookings()
    if not status:
        return response_builder.ok_200().failure().message(message).get_response()

    result = dict(bookings=serialized_bookings)
    return response_builder.ok_200().success().response_data(result).get_response()
