from ola.helper.utils import *
from ola.models import UserAccount


class CustomerProfile:
    def __init__(self, email=None, phone_number=None):
        self.email = email
        self.phone = phone_number

    def get_customer_via_email(self):
        return get_or_none(UserAccount, email=self.email)

    def get_customer_via_phone(self):
        return get_or_none(UserAccount, phone_number=self.phone)

    def check_customer_exists(self):
        user = self.get_customer_via_email()
        if user:
            return 0, "User already exists with the given email"

        user = self.get_customer_via_phone()
        if user:
            return 0, "User already exists with the given number"

        return 1, "User does not exists with the details provided"

    def create_customer_profile(self, password, first_name, gender, dob, last_name=None, isd=None):
        customer = UserAccount.objects.create_user(email=self.email,
                                                   password=password,
                                                   phone=self.phone,
                                                   first_name=first_name,
                                                   gender=gender,
                                                   dob=dob,
                                                   last_name=last_name,
                                                   isd_code=isd)
        return customer
