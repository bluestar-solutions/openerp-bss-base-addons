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
from openerp.tools import logging
from openerp.tools.translate import _
from openerp.addons.bss_hades.request_parameter import (
    DATA_TYPE  # @UnresolvedImport
)
from openerp.addons.bss_parameters.bss_parameter_field import (
    bss_parameter  # @UnresolvedImport
)
import json


class request_parameter_value(osv.TransientModel):
    _name = 'request.parameter.value'
    _description = "Value"
    _logger = logging.getLogger(_name)

    def _get_selection_values(self, cr, uid, ids, field_name,
                              args, context=None):
        res = {}
        for r in self.browse(cr, uid, ids, context):
            if r.selection_version_id:
                res[r.id] = json.dumps([(v.id, v.name) for v in
                                        r.selection_version_id.value_ids])
            else:
                res[r.id] = "[]"
        return res

    _columns = {
        'request_data_id': fields.many2one('request.data', 'Request Data',
                                           required=True),
        'parameter_id': fields.many2one(
            'request.parameter', 'Parameter',
            required=True, ondelete='no action'
        ),
        'name': fields.related(
            'parameter_id', 'name', type="char", string="Name", readonly=True
        ),
        'data_type': fields.related(
            'parameter_id', 'data_type',
            type='selection', selection=DATA_TYPE, readonly=True
        ),
        'required': fields.related(
            'parameter_id', 'required', type='boolean', readonly=True
        ),
        'key': fields.related(
            'parameter_id', 'key', type='char', readonly=True
        ),
        'max_length': fields.related('parameter_id', 'max_length',
                                     type="integer"),
        'selection_version_id': fields.many2one(
            'bss.parameter.selection.version', string="Selection",
            auto_join=True, readonly=True
        ),
        'selection_values': fields.function(
            _get_selection_values, type="char",
            string="Selection Values",
            method=True, store=False, multi=False),
        'value': bss_parameter(
            'Value', data_type='data_type',
            selection_version_id='selection_version_id',
            selection_values='selection_values',
            auto_select_value=True,
            required_field='required',
            max_length_field='max_length'
        ),
    }

request_parameter_value()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
