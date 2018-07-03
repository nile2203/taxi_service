"""taxi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from ola.views import user_views, cab_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/', user_views.api_user_registration, name="create user account for users and drivers"),
    url(r'^driver/documents/upload/', user_views.api_upload_driver_documents, name="upload driver documents"),
    url(r'^driver/bank/details/', user_views.api_register_driver_bank_details, name="register driver bank details"),
    url(r'^booking/history/get/$', user_views.api_get_booking_history, name="get user booking history"),
    url(r'^book/cab/$', cab_views.api_book_cab, name="book cab"),
    url(r'^cabs/get/$', cab_views.api_get_all_available_cabs, name="get all available cabs")
]
