"""
catalog_helpers.py
Contains several utility functions for catalog.py.
"""

from base64 import b64encode
from os import urandom


def correctCasing(words):
    """
    Formats given str to a standard capitalization where
    all the first letters of a word are capitalized.
    """
    strings = words.split(' ')
    strings = [s[0].upper()+s[1:].lower() for s in strings if s]
    return ' '.join(strings)


def generateRandomString():
    """
    Utility function to generate a randomized 32-character utf-8 string.
    """
    return ''.join(b64encode(urandom(32)).decode('utf-8'))
