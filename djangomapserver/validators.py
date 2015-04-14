import re

from django.core.exceptions import ValidationError


def validate_integer_color(val):
    """
    Validates that an integer RGB value is between 0 and 255.
    Prevents error due to out of range RGB values.
    """
    if val < 0 or val > 255:
        raise ValidationError(u'{} is not a valid RGB color integer value.'.format(val))

def validate_hex_color(hex_str):
    """
    Validates an RGB hex string.
    """
    match_str = r'#[0-9a-fA-F]{6}'
    if re.match(match_str, hex_str) is None:
        raise ValidationError(u'{} is not a valid RGB hex string.'.format(hex_str))
