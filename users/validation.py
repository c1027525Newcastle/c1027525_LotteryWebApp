import re
from wtforms.validators import ValidationError


def excludes_character_check(form, name_field):
    """
    Checks and raises an error message, containing all characters that shouldn't have been entered, if the field
    contains any of the excluded characters
    :param form: NOT SURE
    :param name_field: NOT SURE
    :return: Raises validation error message
    """
    # String of characters that should be excluded
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    # String where excluded characters that the user inputted will be place
    not_allowed_chars = ""

    # Checks for each character in name_field if it contains any excluded characters
    for char in name_field.data:
        if char in excluded_chars:
            # Concatenate excluded character to the not_allowed_chars string
            not_allowed_chars = not_allowed_chars + char

    # If not_allowed_chars is not empty it means that there are excluded characters in the name_field so raise error
    if not_allowed_chars != "":
        raise ValidationError(f"Character/s {not_allowed_chars} is/are not allowed")


def contains_check(form, data_field):
    """
    Checks and raises an error message if data_field contains any characters specified in p using regex
    :param form: NOT SURE
    :param data_field: NOT SURE
    :return: Raises validation error message
    """
    # Create the pattern using regex
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')

    # Checks if data_field does not match the pattern of p and raises the error
    if not p.match(data_field.data):
        raise ValidationError("Password need at least 1 digit, 1 lowercase and uppercase character and 1 special "
                              "character e.g. !?% and it can be between 6 and 12 characters")


def phone_format_check(form, phone_field):
    """
    Check and raises an error message if phone_field is not formatted in the specified way using regex
    :param form: NOT SURE
    :param phone_field: NOT SURE
    :return: Raises validation error message
    """
    # Create the pattern using regex
    p = re.compile(r'^[0-9]{4}-[0-9]{3}-[0-9]{4}$')

    # Checks if phone_field does not match the pattern of p and raises the error
    if not p.match(phone_field.data):
        raise ValidationError("Phone number should be written in this format XXXX-XXX-XXXX")
