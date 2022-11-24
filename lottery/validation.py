import re

from flask import flash


def check_draw(draw_number):
    """
    Checks if the draw was entered and is between 1 and 60 and if not flashes
    an appropriate error message and returns True
    :param draw_number: number
    :return: True
    """
    p = re.compile(r'(^[1-9]$)|(^[1-5][0-9]$)|(^60$)')

    if not p.match(draw_number):
        flash('Must contain 6 numbers and each must be between 1 and 60')
        return True
