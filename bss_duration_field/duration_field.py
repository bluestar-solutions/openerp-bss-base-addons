# -*- encoding: utf-8 -*-
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

from math import floor
from re import match

from odoo import fields, models
from odoo.osv import osv
from odoo.tools.translate import _


CONVERSIONS = {
    'w': lambda x: float(x) * 5.0,  # week(s) in days
    'd': lambda x: float(x),  # day(s) in days
    'h': lambda x: float(x) / 24.0  # hour(s) in days
}

PATTERNS = None


class duration(fields.Float):
    _type = 'duration'
    _symbol_c = '%s'

    def _symbol_f(x):  # @NoSelf
        return duration.parse_value(x)

    _symbol_set = (_symbol_c, _symbol_f)

    @staticmethod
    def init_patterns():
        PATTERNS = ""
        pattern = r'^\d{1,}%s$'

        conv_keys = CONVERSIONS.viewkeys()

        while(len(conv_keys) > 0):
            PATTERNS += (pattern % conv_keys.pop())
            if len(conv_keys) > 0:
                PATTERNS += "|"

    @staticmethod
    def validate_str(str_to_validate):
        if PATTERNS is None:
            duration.init_patterns()

        for element in str_to_validate.split(' '):
            if match(PATTERNS, element) is None:
                return False

        return True

    @staticmethod
    def parse_value(vals):
        if not duration.validate_str(vals):
            raise osv.except_osv(
                _("Error!"),
                _("String duration is not valid.")
            )

        total = float(0.0)

        for element in vals.split(' '):
            total += CONVERSIONS[element[-1]](element[:-1])

        return total

    def __init__(self, string="unknown", **args):
        fields.float.__init__(self, string=string, **args)

    def _symbol_get(self, value_to_display):
        days = int(floor(value_to_display))
        hours = int((value_to_display - days) * 24)

        return "%sd %sh" % (days, hours)

fields.duration = duration

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
