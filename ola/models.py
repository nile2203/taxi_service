import uuid

from datetime import datetime
from django.db import models

from geoposition.fields import GeopositionField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

# Create your models here.


def get_24_char_uuid():
    uid = uuid.uuid4().hex
    for i in range(0, 8):
        uid = uid[:i] + uid[i + 1:]
    return uid.upper()


class UserAccountManager(BaseUserManager):
    def create_user(self,
                    email,
                    password=None,
                    first_name=None,
                    phone=None,
                    gender=None,
                    dob=None,
                    last_name=None,
                    isd_code=None,
                    **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=dob,
            phone_number=phone,
            isd_code=isd_code,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    STATUS_VERIFIED = 'VERIFIED'
    STATUS_PENDING = 'PENDING'
    STATUS_PROCESSING = 'PROCESSING'
    STATUS_REJECTED = 'REJECTED'

    status_choices = ((STATUS_VERIFIED, 'VERIFIED'),
                      (STATUS_PENDING, 'PENDING'),
                      (STATUS_PROCESSING, 'PROCESSING'),
                      (STATUS_REJECTED, 'REJECTED')
    )
    GENDER_MALE = "MALE"
    GENDER_FEMALE = "FEMALE"
    GENDER_TRANSGENDER = "TRANSGENDER"

    gender_choices = (
        (GENDER_MALE, "MALE"),
        (GENDER_FEMALE, "FEMALE"),
        (GENDER_TRANSGENDER, "TRANSGENDER"),
    )

    TYPE_USER = "USER"
    TYPE_DRIVER = "DRIVER"

    type_choices = (
        (TYPE_USER, "USER"),
        (TYPE_DRIVER, "DRIVER")
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_id = models.CharField(max_length=100, blank=False, unique=True, default=get_24_char_uuid)
    type = models.CharField(max_length=10, default=TYPE_USER, choices=type_choices)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    isd_code = models.CharField(max_length=4, default='91', null=True)
    gender = models.CharField(max_length=15, blank=True, null=True, default=GENDER_MALE, choices=gender_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    driver_id = models.CharField(max_length=10, blank=True, null=True)
    profile_status = models.CharField(max_length=20, default=STATUS_PENDING, choices=status_choices)

    objects = UserAccountManager()
    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type', 'phone_number']

    def __unicode__(self):
        fields = [self.first_name, self.last_name, self.email]
        return " ".join(fields)

    def save(self, *args, **kwargs):
        super(UserAccount, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        unique_together = ('email', 'type')


class Cab(models.Model):
    HATCHBACK = "HATCHBACK"
    SEDAN = "SEDAN"
    SUV = "SUV"
    PREMIUM_SEDAN = "PREMIUM SEDAN"

    NATIONAL_PERMIT = "NATIONAL PERMIT"
    STATE_PERMIT = "STATE PERMIT"

    STATUS_WORKING = "WORKING"
    STATUS_NOT_WORKING = "NOT WORKING"

    TYPE_MINI = "MINI"
    TYPE_PRIME = "PRIME"
    TYPE_LUXURY = "LUXURY"

    service_type_choices = (
        (TYPE_MINI, "MINI"),
        (TYPE_PRIME, "PRIME"),
        (TYPE_LUXURY, "LUXURY")
    )
    service_status_choices = (
        (STATUS_WORKING, "WORKING"),
        (STATUS_NOT_WORKING, "NOT WORKING")
    )
    permit_level_choices = (
        (NATIONAL_PERMIT, "NATIONAL PERMIT"),
        (STATE_PERMIT, "STATE PERMIT"),
    )
    cab_type_choices = (
        (HATCHBACK, "HATCHBACK"),
        (SEDAN, "SEDAN"),
        (SUV, "SUV"),
        (PREMIUM_SEDAN, "PREMIUM_SEDAN")
    )

    driver = models.OneToOneField('UserAccount', on_delete=models.CASCADE)
    cab_number = models.CharField(max_length=15, unique=True)
    permit_level = models.CharField(max_length=20, default=NATIONAL_PERMIT, choices=permit_level_choices)
    capacity = models.IntegerField(default=4, blank=True, null=True)
    cab_type = models.CharField(max_length=10, default=HATCHBACK, choices=cab_type_choices)
    state = models.CharField(max_length=15, blank=True, null=True)
    available = models.BooleanField(default=True)
    service_status = models.CharField(max_length=20, default=STATUS_WORKING, choices=service_status_choices)
    service_type = models.CharField(max_length=10, default=TYPE_MINI, choices=service_type_choices)
    color = models.CharField(max_length=20, blank=True, null=True)
    ac = models.BooleanField(default=True)
    location = GeopositionField()

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    def __unicode__(self):
        return self.driver.email + " " + self.cab_number

    class Meta:
        verbose_name = 'Cab'
        verbose_name_plural = 'Cabs'


class BankDetail(models.Model):
    SBI = "STATE BANK OF INDIA"
    HDFC = "HDFC BANK"
    ICICI = "ICICI BANK"
    AXIS = "AXIS BANK"
    BOB = "BANK OF BARODA"
    VB = "VIJAYA BANK"
    PNB = "PUNJAB NATIONAL BANK"

    bank_name_choices = (
        (SBI, "STATE BANK OF INDIA"),
        (HDFC, "HDFC BANK"),
        (ICICI, "ICICI BANK"),
        (AXIS, "AXIS BANK"),
        (BOB, "BANK OF BARODA"),
        (VB, "VIJAYA BANK"),
        (PNB, "PUNJAB NATIONAL BANK"),
    )

    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50, default=SBI, choices=bank_name_choices)
    account_number = models.CharField(max_length=20, blank=True, null=False)
    branch_name = models.CharField(max_length=50, blank=True, null=False)
    ifsc_code = models.CharField(max_length=20, blank=True)
    micr_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    def __unicode__(self):
        fields = [self.bank_name, self.ifsc_code]
        return " ".join(fields)

    class Meta:
        verbose_name = 'Bank Detail'
        verbose_name_plural = 'Bank Details'


class DriverDocument(models.Model):
    DRIVING_LICENCE = 'DRIVING LICENCE'
    VEHICLE_PERMIT = 'VEHICLE PERMIT'
    PAN_CARD = 'PAN CARD'
    AADHAAR_CARD = 'AADHAAR CARD'
    CHEQUE = 'CHEQUE'
    PASSBOOK = 'PASSBOOK'
    VEHICLE_INSURANCE = 'VEHICLE INSURANCE'
    VEHICLE_RC = "VEHICLE RC"

    document_choices = (
        (DRIVING_LICENCE, 'DRIVING LICENCE'),
        (VEHICLE_PERMIT, 'VEHICLE PERMIT'),
        (VEHICLE_INSURANCE, 'VEHICLE INSURANCE'),
        (PAN_CARD, 'PAN CARD'),
        (AADHAAR_CARD, 'AADHAAR CARD'),
        (CHEQUE, 'CHEQUE'),
        (PASSBOOK, 'PASSBOOK'),
        (VEHICLE_RC, 'VEHICLE RC')
    )

    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, default=DRIVING_LICENCE, choices=document_choices)
    description = models.TextField(max_length=100, blank=True, null=True)
    document_url = models.TextField(max_length=200, blank=True, null=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    def __unicode__(self):
        fields = [self.driver.email, self.document_type]
        return " ".join(fields)

    class Meta:
        verbose_name = 'Driver Document'
        verbose_name_plural = 'Driver Documents'


class BookingHistory(models.Model):
    STATUS_REQUESTING = "REQUESTING"
    STATUS_BOOKED = "BOOKED"
    STATUS_RIDING = "RIDING"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_COMPLETED = "COMPLETED"

    status_choices = (
        (STATUS_REQUESTING, "REQUESTING"),
        (STATUS_BOOKED, "BOOKED"),
        (STATUS_RIDING, "RIDING"),
        (STATUS_CANCELLED, "CANCELLED"),
        (STATUS_COMPLETED, "COMPLETED")
    )

    user = models.ForeignKey('UserAccount', related_name='user', on_delete=models.CASCADE)
    driver = models.ForeignKey('UserAccount', related_name='driver', on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=24, default=get_24_char_uuid, blank=False)
    fare = models.FloatField(default=0.0)
    starting_point = models.TextField(max_length=100, blank=True, null=True)
    ending_point = models.TextField(max_length=100, blank=True, null=True)
    date_of_booking = models.DateField(null=True, blank=True)
    duration = models.TimeField()
    status = models.CharField(max_length=20, default=STATUS_REQUESTING, choices=status_choices)
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE)
    cab = models.OneToOneField('Cab', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.email + " " + self.booking_id

    class Meta:
        verbose_name = 'Booking History'
        verbose_name_plural = 'Booking Histories'


class Rating(models.Model):
    stars = models.IntegerField(default=0, blank=True, null=True)
    comment = models.TextField(max_length=200, blank=True, null=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    def __unicode__(self):
        fields = [self.booking_id, self.stars]
        return " ".join(fields)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class OTPDetail(models.Model):
    otp = models.IntegerField(blank=False, null=False, default='000000')
    user = models.OneToOneField('UserAccount', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        fields = [self.user.phone_number, self.otp]
        return " ".join(fields)

    class Meta:
        verbose_name = 'OTP Detail'
        verbose_name_plural = 'OTP Details'


class DiscountCoupon(models.Model):
    TYPE_OLD_USER = "OLD USER"
    TYPE_NEW_USER = "NEW USER"

    type_choices = (
        (TYPE_NEW_USER, "NEW USER"),
        (TYPE_OLD_USER, "OLD USER")
    )

    coupon_code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=10, default=TYPE_OLD_USER, choices=type_choices)
    coupon_value = models.IntegerField(default=0)
    validity = models.DateField(default=datetime.now)
    description = models.TextField(max_length=100, blank=True, null=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    def __unicode__(self):
        return self.coupon_code

    class Meta:
        verbose_name = 'Discount Coupon'
        verbose_name_plural = 'Discount Coupons'
