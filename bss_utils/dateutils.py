# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2015 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
import time
from openerp.addons.bss_utils.decorator import deprecated  # @UnresolvedImport

ORM_DATE_FORMAT = '%Y-%m-%d'
ORM_TIME_FORMAT = '%H:%M:%S'
ORM_DATETIME_FORMAT = '%s %s' % (ORM_DATE_FORMAT, ORM_TIME_FORMAT)


def orm2datetime(value, tformat=ORM_DATETIME_FORMAT):
    """Return a datetime object from an ORM datetime string value"""
    return datetime.strptime(value, tformat)


def orm2date(value, tformat=ORM_DATE_FORMAT):
    """Return a date object from an ORM date string value"""
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


@deprecated
def orm_datetime(value):
    return orm2datetime(value)


@deprecated
def orm_date(value):
    return orm2datetime(value, tformat=ORM_DATE_FORMAT)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
