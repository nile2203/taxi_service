# Generated by Django 2.0 on 2018-07-02 04:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import geoposition.fields
import ola.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(choices=[('STATE BANK OF INDIA', 'STATE BANK OF INDIA'), ('HDFC BANK', 'HDFC BANK'), ('ICICI BANK', 'ICICI BANK'), ('AXIS BANK', 'AXIS BANK'), ('BANK OF BARODA', 'BANK OF BARODA'), ('VIJAYA BANK', 'VIJAYA BANK'), ('PUNJAB NATIONAL BANK', 'PUNJAB NATIONAL BANK')], default='STATE BANK OF INDIA', max_length=50)),
                ('account_number', models.CharField(blank=True, max_length=20)),
                ('branch_name', models.CharField(blank=True, max_length=50)),
                ('ifsc_code', models.CharField(blank=True, max_length=20)),
                ('micr_code', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Bank Detail',
                'verbose_name_plural': 'Bank Details',
            },
        ),
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(default=ola.models.get_24_char_uuid, max_length=24)),
                ('fare', models.FloatField(default=0.0)),
                ('starting_point', geoposition.fields.GeopositionField(max_length=42)),
                ('ending_point', geoposition.fields.GeopositionField(max_length=42)),
                ('date_of_booking', models.DateField(blank=True, null=True)),
                ('duration', models.TimeField()),
                ('status', models.CharField(choices=[('REQUESTING', 'REQUESTING'), ('BOOKED', 'BOOKED'), ('RIDING', 'RIDING'), ('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED')], default='REQUESTING', max_length=20)),
            ],
            options={
                'verbose_name': 'Booking History',
                'verbose_name_plural': 'Booking Histories',
            },
        ),
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cab_number', models.CharField(max_length=15, unique=True)),
                ('permit_level', models.CharField(choices=[('NATIONAL PERMIT', 'NATIONAL PERMIT'), ('STATE PERMIT', 'STATE PERMIT')], default='NATIONAL PERMIT', max_length=20)),
                ('capacity', models.IntegerField(blank=True, default=4, null=True)),
                ('cab_type', models.CharField(choices=[('HATCHBACK', 'HATCHBACK'), ('SEDAN', 'SEDAN'), ('SUV', 'SUV'), ('PREMIUM SEDAN', 'PREMIUM_SEDAN')], default='HATCHBACK', max_length=10)),
                ('state', models.CharField(blank=True, max_length=15, null=True)),
                ('available', models.BooleanField(default=True)),
                ('service_status', models.CharField(choices=[('WORKING', 'WORKING'), ('NOT WORKING', 'NOT WORKING')], default='WORKING', max_length=20)),
                ('service_type', models.CharField(choices=[('MINI', 'MINI'), ('PRIME', 'PRIME'), ('LUXURY', 'LUXURY')], default='MINI', max_length=10)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('ac', models.BooleanField(default=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Cab',
                'verbose_name_plural': 'Cabs',
            },
        ),
        migrations.CreateModel(
            name='DiscountCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(blank=True, max_length=10, null=True)),
                ('type', models.CharField(choices=[('NEW USER', 'NEW USER'), ('OLD USER', 'OLD USER')], default='OLD USER', max_length=10)),
                ('coupon_value', models.IntegerField(default=0)),
                ('validity', models.DateField(default=datetime.datetime.now)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Discout Coupon',
                'verbose_name_plural': 'Discount Coupons',
            },
        ),
        migrations.CreateModel(
            name='DriverDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docuemnt_type', models.CharField(choices=[('DRIVING LICENCE', 'DRIVING LICENCE'), ('VEHICLE PERMIT', 'VEHICLE PERMIT'), ('VEHICLE INSURANCE', 'VEHICLE INSURANCE'), ('PAN CARD', 'PAN CARD'), ('AADHAAR CARD', 'AADHAAR CARD'), ('CHEQUE', 'CHEQUE'), ('PASSBOOK', 'PASSBOOK'), ('VEHICLE RC', 'VEHICLE RC')], default='DRIVING LICENCE', max_length=20)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Driver Document',
                'verbose_name_plural': 'Driver Documents',
            },
        ),
        migrations.CreateModel(
            name='OTPDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.IntegerField(default='000000')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'OTP Detail',
                'verbose_name_plural': 'OTP Details',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField(blank=True, max_length=200, null=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('user_id', models.CharField(default=ola.models.get_24_char_uuid, max_length=100, unique=True)),
                ('type', models.CharField(choices=[('USER', 'USER'), ('DRIVER', 'DRIVER')], default='USER', max_length=10)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('isd_code', models.CharField(default='91', max_length=4, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('TRANSGENDER', 'TRANSGENDER')], default='MALE', max_length=15, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('driver_id', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_status', models.CharField(choices=[('VERIFIED', 'VERIFIED'), ('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=20)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True)),
                ('bank_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ola.BankDetail')),
                ('bookings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ola.BookingHistory')),
                ('documents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ola.DriverDocument')),
            ],
            options={
                'verbose_name': 'User Account',
                'verbose_name_plural': 'User Accounts',
            },
        ),
        migrations.AddField(
            model_name='otpdetail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ola.UserAccount'),
        ),
        migrations.AddField(
            model_name='cab',
            name='driver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ola.UserAccount'),
        ),
        migrations.AddField(
            model_name='bookinghistory',
            name='rating',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ola.Rating'),
        ),
        migrations.AlterUniqueTogether(
            name='useraccount',
            unique_together={('email', 'phone_number')},
        ),
    ]
