import re

from flask import flash


def check_draw(draw_number):
    """
    Checks if the draw is between 1 and 60
    :param draw_number: number
    :return: flash appropriate error message
    """
    p = re.compile(r'(^[0-9]$)|(^[1-6][0-9]$)')

    if not p.match(draw_number):
        return flash('Each number must be between 1 and 60')
