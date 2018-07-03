from datetime import datetime


def get_date_for_dob(date_string):
    return datetime.strptime(date_string, "%d-%m-%Y")


def get_user_readable_date(date_object):
    return datetime.strftime(date_object, '%d %b, %Y')


def get_current_date():
    return datetime.now().date()
