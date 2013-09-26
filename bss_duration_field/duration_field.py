# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from openerp.osv import fields, osv
from openerp.netsvc import logging
from datetime import datetime, timedelta
from math import floor
from re import match

CONVERSIONS = {
               'w': lambda x: float(x)*5.0,     # week(s) in days
               'd': lambda x: float(x),         # day(s) in days
               'h': lambda x: float(x)/24.0     # hour(s) in days
               }

class duration(fields.float):
    _type = 'duration'
    _symbol_c = '%s'
    _symbol_f = lambda x: duration.parse_value(x)
    _symbol_set = (_symbol_c,_symbol_f)
    
    @staticmethod
    def validate_str(str_to_validate):
        pattern = r'^\d{1,}%s$'
        elements = str_to_validate.split(' ')
        result = True
        
        for element in elements:
            tmp = False
            for conv in CONVERSIONS.iterkeys():
                tmp = tmp or (match(pattern % conv,element) is not None)
            result = result and tmp 
        
        return result
    
    @staticmethod    
    def parse_value(vals):
        if not duration.validate_str(vals):
            raise osv.except_osv("Validation error", "String duration is not valid !")
        
        total = float(0.0)
        elements = vals.split(' ')
        
        for element in elements:
            total += CONVERSIONS[element[-1]](element[:-1])
        
        return total
    
    def __init__(self, string="unknown", **args):
        fields.float.__init__(self, string=string, **args)

    def _symbol_get(self, value_to_display):
        days = int(floor(value_to_display))
        hours = int((value_to_display - days)*24)
        
        return "%sd %sh" % (days, hours)

fields.duration = duration