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
from re import match

class bss_parser(osv.TransientModel):
    _name = "bss_duration_widget.bss_parser"
    _description = "Parser and validator for duration"

    @staticmethod
    def _validate_str(self, str_to_validate):
        rex = r'^[0-9]{1,}d$|^[0-9]{1,}h?$|^[0-9]{1,}d\ [0-9]{1,2}h$'
        
        return match(rex, str_to_validate) is not None
    
    @staticmethod
    def parse_str(self, str_to_parse):
        if not self._validate_str(str_to_parse):
            raise osv.except_osv("Validation error", "String duration is not valid !")
        
        td = timedelta()
        elements = str_to_parse.split(' ')
        
        for element in elements:
            if element[-1] == 'd':
                td += timedelta(days=element[:-1])
            elif element[-1] == 'h':
                td += timedelta(hours=element[:-1])
        
        return td.total_seconds()

    @staticmethod
    def display_value(self, value_to_display):
        if type(value_to_display) in [str,int]:
            value_to_display = float(value_to_display)
        elif type(value_to_display) == datetime:
            value_to_display = float((value_to_display-datetime(1970,1,1)).total_seconds())
        
        return "%sd %sh" % (int(value_to_display//(60.0*60.0*24.0)),int(value_to_display%(60.0*60.0*24.0)))