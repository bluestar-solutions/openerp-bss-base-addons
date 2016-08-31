# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from openerp.osv import osv, fields
from openerp.netsvc import logging
from openerp.tools.translate import _
import re

DATA_TYPE = (('integer', 'Integer'),
             ('decimal', 'Decimal'),
             ('boolean', 'Boolean'),
             ('time', 'Time'),
             ('text', 'Text'),
             ('selection', 'Selection'),)

RE_VALID_TIME = re.compile(r'^([0-9]*):?([0-5]?[0-9])?$')


class ValueValidationException(Exception):
    pass


class request_parameter(osv.osv):
    _name = 'request.parameter'
    _description = "Request Parameter"
    _logger = logging.getLogger(_name)

    _columns = {
        'name': fields.char('Name', size=256, translate=True, required=True),
        'data_type': fields.selection(DATA_TYPE, 'Data Type', required=True),
        'format': fields.char('Format', size=16),
        'selection_id': fields.many2one('bss.parameter.selection', "Selection",
                                        auto_join=True),
        # TODO: Move required field in many2many table
        'required': fields.boolean('Required'),
        'max_length': fields.integer('Max Length'),
        'key': fields.char('Key', size=64, required=True),
    }

    _defaults = {
        'data_type': 'decimal',
        'format': ':.3f',
    }

    _sql_constraints = [
        ('key', 'unique(key)', 'Key must be unique!'),
        ('selection_id_unique', 'unique(selection_id)',
         'Selection must be unique!'),
    ]

    def get_by_key(self, cr, uid, key, context=None):
        res_ids = self.search(cr, uid, [('key', '=', key)],
                              limit=1, context=context)
        if res_ids:
            return self.browse(cr, uid, res_ids[0], context)
        return None

    def _split_time(self, value):
        m = RE_VALID_TIME.match(value or '')
        if not m:
            raise ValueError()
        return int(m.group(1) or '0'), int(m.group(2) or '0')

    def _is_floatable(self, data_type):
        return data_type in ('integer', 'decimal', 'time')

    def _to_float(self, data_type, value):
        if data_type == 'integer':
            return int(value)
        if data_type == 'decimal':
            return float(value)
        if data_type == 'time':
            hours, minutes = self._split_time(value)
            return round(hours + minutes / 60.0, 4)

    def _validate_mandatory(self, name, data_type, required, value):
        if required and data_type != 'boolean' and value is False:
            raise ValueValidationException(
                _('%(parameter)s: must be defined.') % {
                    'parameter': name,
                }
            )

    def _validate_integer(self, name, value, **args):
        if not value:
            return ''
        try:
            return str(int(value))
        except ValueError as e:
            self._logger.debug(e, exc_info=True)
            raise ValueValidationException(
                _("%s must be an integer value.") % name
            )

    def _validate_decimal(self, name, value, decimal_format=':.3f', **args):
        if not value:
            return ''
        try:
            return ('{%s}' % decimal_format).format(float(value))
        except ValueError as e:
            self._logger.debug(e, exc_info=True)
            raise ValueValidationException(
                _("%s must be a decimal number value.") % name
            )

    def _validate_time(self, name, value, **args):
        if not value:
            return ''
        try:
            hours, minutes = self._split_time(value)
            return '%d:%02d' % (hours, minutes or 0)
        except ValueError as e:
            self._logger.debug(e, exc_info=True)
            raise ValueValidationException(
                _("%s must be a time value (hours:minutes).") % name
            )

    def _validate_text(self, name, value, max_length=None, **args):
        if not value:
            return ''
        if max_length and len(value) > max_length:
            raise ValueValidationException(
                _("%s cannot be longer than %d.") % (name, max_length)
            )
        return value

    def validate_value(self, name, data_type, required,
                       decimal_format, max_length, value):
        self._validate_mandatory(name, data_type, required, value)
        validate = {
            'integer': self._validate_integer,
            'decimal': self._validate_decimal,
            'boolean': lambda __, v, **a: v,
            'selection': lambda __, v, **a: v,
            'time': self._validate_time,
            'text': self._validate_text,
        }
        return validate[data_type](
            name, value, decimal_format=decimal_format, max_length=max_length
        )

request_parameter()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
