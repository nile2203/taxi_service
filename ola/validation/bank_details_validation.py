import re


def validate_bank_information(**data):
    if not data:
        return 0, "Please provide data to validate"

    status, message = validate_ifsc(data.get('ifsc'))
    if not status:
        return 0, message
    status, message = validate_micr(data.get('micr'))
    if not status:
        return 0, message
    status, message = validate_account_number(data.get('account'))
    if not status:
        return 0, message
    return 1, "All information is valid"


def validate_ifsc(ifsc):
    pattern = re.compile("^([A-Z]{4}\d{7})")
    if not pattern.match(ifsc):
        return 0, "IFSC Code is invalid"
    return 1, "IFSC Code is valid"


def validate_account_number(account_number):
    pattern = re.compile("^(\d{9,18})")
    if not pattern.match(account_number):
        return 0, "Account Number format is invalid"
    return 1, "Account Number format is valid"


def validate_micr(micr):
    pattern = re.compile("^(\d{9})")
    if not pattern.match(micr):
        return 0, "Micr code is invalid"
    return 1, "Micr code is valid"
