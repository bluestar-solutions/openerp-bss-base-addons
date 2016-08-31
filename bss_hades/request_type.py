# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2016 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
import re

SIMPLE_REQUEST = r"^SELECT (.*) FROM .*;$"
SIMPLE_PATTERN = re.compile(SIMPLE_REQUEST, re.IGNORECASE)


# TODO: Move method in utils
def ref_id(obj, cr, uid, xml_id):
    """Return a database id for an xml_id (with module name)"""
    return obj.pool.get('ir.model.data').get_object_reference(
        cr, uid, *xml_id.split('.')
    )[1]


class request_type(osv.Model):
    _name = 'request.type'
    _description = "Request Type"
    _logger = logging.getLogger(_name)

    # TODO: Process column headers with order unless *
    def _get_headers(self, cr, uid, ids, field_name, args, context=None):
        return dict.fromkeys(ids, None)
        # TODO: Process aliases
        res = {}
        for req in self.browse(cr, uid, ids, context):
            res[req.id] = SIMPLE_PATTERN.match(req.request).group(1)

        return res

    # TODO: Improve validation (Prepared query)
    def _is_request_valid(self, cr, uid, ids, context=None):
        return True
        for req in self.browse(cr, uid, ids, context):
            if len(req.request.split(';')) > 2:
                return False
            if not SIMPLE_PATTERN.match(req.request):
                return False
        return True

    def exec_request(self, cr, uid, ids, context=None):
        if isinstance(ids, list):
            ids = ids[0]

        if not context:
            context = {}

        data_id = self.pool.get('request.data').create(
            cr, uid, {'request_type_id': ids}, context
        )

        form_id = ref_id(self, cr, uid,
                         'bss_hades.view_request_data_form')
        return {
            'name': 'Request Data',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'res_id': data_id,
            'res_model': 'request.data',
            'views': [(form_id, 'form')],
            'view_mode': 'form',
        }

    _columns = {
        'name': fields.char('Name', required=True),
        'request': fields.text('SQL Request', required=True),
        'headers': fields.function(_get_headers, type="char",
                                   method=True, store=False, string="Headers"),
        'parameter_ids': fields.many2many('request.parameter',
                                          'request_type_parameter_rel',
                                          'request_type_id',
                                          'request_parameter_id',
                                          string="Parameters"),
    }

    _constraints = [(_is_request_valid, "Error", "Request is not valid!")]

request_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
