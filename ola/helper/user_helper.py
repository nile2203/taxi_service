from ola.helper import datetime_helper


def format_email(email):
    if email:
        return email.lower()


def format_dob(dob):
    return datetime_helper.get_date_for_dob(dob)
