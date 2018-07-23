"""
    JS URLs text utilities
    ======================

    This modules defines utilities allowing to text and strings.

"""

from functools import reduce


def replace(data, replacements):
    """ Allows to performs several string substitutions.

    This function performs several string substitutions on the initial ``data`` string using a list
    of 2-tuples (old, new) defining substitutions and returns the resulting string.

    """
    return reduce(lambda a, kv: a.replace(*kv), replacements, data)
