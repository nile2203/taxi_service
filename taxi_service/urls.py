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

    path('v1/api/user/register/', user_views.UserAccountRegistrationView.as_view()),
    path('v1/api/user/bank/details/', user_views.BankDetailsView.as_view()),
    path('v1/api/user/booking/history/', user_views.GetBookingHistoryView.as_view()),
    path('v1/api/cab/', cab_views.RegisterCabView.as_view()),
    path('v1/api/cab/available/', cab_views.AvailableCabView.as_view()),
    path('v1/api/cab/book/', cab_views.BookCabView.as_view())

]
