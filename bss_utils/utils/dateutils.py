# -*- coding: utf-8 -*-
# Part of Python Utilities.
# See LICENSE file for full copyright and licensing details.

from datetime import datetime, date
import time

ORM_DATE_FORMAT = '%Y-%m-%d'
ORM_TIME_FORMAT = '%H:%M:%S'
ORM_DATETIME_FORMAT = '%s %s' % (ORM_DATE_FORMAT, ORM_TIME_FORMAT)


def orm2datetime(value, tformat=ORM_DATETIME_FORMAT, default=None):
    """Return a datetime object from an ORM datetime string value"""
    if not value:
        return default
    return datetime.strptime(value, tformat)


def orm2date(value, tformat=ORM_DATE_FORMAT, default=None):
    """Return a date object from an ORM date string value"""
    if not value:
        return default
    return datetime.strptime(value, tformat).date()


def timestamp(millis=False):
    """Return current int timestamp (with or without millisecond)"""
    return int(round(time.time() * (millis and 1000 or 1)))


def datetime2timestamp(value, millis=False):
    """Return an int timestamp from a datetime (with or without millisecond)"""
    if millis:
        return int(time.mktime(value.timetuple()))
    else:
        return int(round((time.mktime(value.timetuple()) +
                          value.microsecond / 1E6) * 1000))


def timestamp2datetime(value, millis=False):
    """Return a datetime from a int timestamp (with or without millisecond)"""
    return datetime.fromtimestamp(value / (millis and 1000. or 1))


def get_quarter_start(date_at):
    quarter_month = ((date_at.month - 1) / 3) * 3 + 1
    return date(date_at.year, quarter_month, 1)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
