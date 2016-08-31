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
from openerp.tools.translate import _
import base64
import tablib

ACTIONS = ['export_to_csv', 'export_to_xlsx', 'view']


# TODO: Move method in utils
def ref_id(obj, cr, uid, xml_id):
    """Return a database id for an xml_id (with module name)"""
    return obj.pool.get('ir.model.data').get_object_reference(
        cr, uid, *xml_id.split('.')
    )[1]


class request_data(osv.TransientModel):
    _name = 'request.data'
    _description = "Request Data"
    _logger = logging.getLogger(_name)

    def _has_parameters(self, cr, uid, ids, field_name, args, context=None):
        res = {}

        for rec in self.browse(cr, uid, ids, context):
            res[rec.id] = bool(rec.parameter_value_ids and
                               len(rec.parameter_value_ids) > 0)

        return res

    _columns = {
        'name': fields.related('request_type_id', 'name', type="char",
                               readonly=True),
        'request_type_id': fields.many2one('request.type', 'Request Type',
                                           required=True, readonly=True),
        'parameter_value_ids': fields.one2many('request.parameter.value',
                                               'request_data_id',
                                               string="Parameter Values"),
        'has_parameters': fields.function(_has_parameters, type="boolean",
                                          method=True, store=False,
                                          string="Has Parameters"),
    }

    def create(self, cr, uid, vals, context=None):
        super(request_data, self).default_get(cr, uid, vals, context)
        rt_id = vals.get('request_type_id')

        if not rt_id:
            raise osv.except_osv(_("Error!"),
                                 _("Cannot process empty request_type_id"))

        rt = self.pool.get('request.type').browse(cr, uid,
                                                  rt_id, context)

        if rt.parameter_ids:
            vals['parameter_value_ids'] = [(0, 0, {'parameter_id': param.id})
                                           for param in rt.parameter_ids]

        return super(request_data, self).create(cr, uid, vals, context)

    def _get_datas(self, cr, uid, ids, context=None):
        if isinstance(ids, list):
            ids = ids[0]

        # print "psycopg cursor:", cr._obj, type(cr._obj)

        req_data = self.browse(cr, uid, ids, context)
        headers = req_data.request_type_id.headers
        request = req_data.request_type_id.request

        params = {param.key: param.value or None
                  for param in req_data.parameter_value_ids}
        params['uid'] = uid
        # TODO: Eventually add more "global" parameters

        req_result = None

        try:
            cr.execute(request, params)
            req_result = cr.dictfetchall()
        except:
            raise osv.except_osv(
                _("Error!"),
                _("An error occured when requesting the database.")
            )

        return headers, req_result

    def get_datas(self, cr, uid, request_data_id, context=None):
        if not request_data_id:
            return None

        headers, datas = self._get_datas(cr, uid, request_data_id, context)
        if datas:
            # TODO: Remove "or True" when headers are properly parsed
            if headers == '*' or True:
                headers = datas[0].keys()
                if "id" in headers:
                    headers.remove("id")
                    headers.insert(0, "id")
            else:
                headers = headers.split(',')
        else:
            datas = []
            headers = []

        return {'datas': datas, 'headers': headers}

    def _export_data(self, cr, uid, req_result,
                     name, data_format="csv", context=None):
        if not req_result:
            return False

        data = tablib.Dataset()
        data.dict = req_result
        content = base64.encodestring(getattr(data, data_format))

        if content:
            # TODO: Add date/time in file name ?
            wizard_id = self.pool.get('download.wizard').create(
                cr, uid,
                {'generated_file_stream': content,
                 'generated_file_name': '%s.%s' % (name, data_format)},
                context=context)

            return {
                'name': 'Download File',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wizard_id,
                'res_model': 'download.wizard',
                'view_mode': 'form',
            }

        return False

    def execute(self, cr, uid, ids, context=None):
        if not context:
            context = {}

        if isinstance(ids, list):
            ids = ids[0]

        action = context.get('req_action')

        if not action or action not in ACTIONS:
            raise osv.except_osv(
                _("Error!"),
                _("Action %s is not valid.") % action
            )

        __, req_result = self._get_datas(cr, uid, ids, context)

        if action.startswith('export_to_'):
            return self._export_data(cr, uid, req_result,
                                     "Test", action[10:], context)
        elif action == 'view':
            form_id = ref_id(self, cr, uid,
                             'bss_hades.view_request_data_qweb')
            return {
                'name': 'View Request',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': ids,
                'res_model': 'request.data',
                'views': [(form_id, 'form')],
                'view_mode': 'form',
            }

        return False

request_data()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
