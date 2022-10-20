import re
from wtforms.validators import ValidationError


def excludes_character_check(form, field):
    """
    Checks and raises an error message if the field contains any of the excluded characters
    :param form: NOT SURE
    :param field: NOT SURE
    :return: Raises validation error message
    """
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed, try again")


def contains_check(form, data_field):
    """
    Checks and raises an error message if data_field contains any characters specified in p using regex
    :param form: NOT SURE
    :param data_field: NOT SURE
    :return: Raises validation error message
    """
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')

    if not p.match(data_field.data):
        raise ValidationError("Password need at least 1 digit, 1 lowercase and uppercase character and 1 special "
                              "character")


def phone_format_check(form, phone_field):
    """
    Check and raises an error message if phone_field is not formatted in the specified way using regex
    :param form: NOT SURE
    :param phone_field: NOT SURE
    :return: Raises validation error message
    """
    p = re.compile(r'^[0-9]{4}-[0-9]{3}-[0-9]{4}$')

    if not p.match(phone_field.data):
        raise ValidationError("Phone number should be written in this format XXXX-XXX-XXXX")
