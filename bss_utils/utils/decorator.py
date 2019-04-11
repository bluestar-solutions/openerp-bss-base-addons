# -*- coding: utf-8 -*-
# Part of Python Utilities.
# See LICENSE file for full copyright and licensing details.

from odoo.netsvc import logging

logger = logging.getLogger('deprecated')


def deprecated(func):
    """A deprecated method decorator.

    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    def new_func(*args, **kwargs):
        logger.warning("Call to deprecated function %s.", func.__name__)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func
