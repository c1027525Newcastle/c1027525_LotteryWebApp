import re

from flask import flash


def check_draw(check, draw_number):
    """
    Checks if the draw is between 1 and 60
    :param check_if_error:
    :param draw_number: number
    :return: flash appropriate error message
    """
    p = re.compile(r'(^[0-9]$)|(^[1-5][0-9]$)|(60)')

    if not p.match(draw_number):
        check = True
        return check, flash('Each number must be between 1 and 60')
