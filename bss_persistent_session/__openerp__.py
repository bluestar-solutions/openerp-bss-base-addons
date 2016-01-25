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

{
    'name': 'bss_persistent_session',
    'version': '7.0.1.0',
    'category': 'Bluestar/Generic module',
    'author': 'Daniel Le Gall',
    'summary': 'Never let webserver session expires',
    'description': """
        This module constantly do RPC requests to retrieve delay between
        two requests. It prevents the webserver to close the session
        because of inactivity. The delay between each request is a
        configuration parameter in ir.config_parameter, configurable
        via the interface in Configuration > Technical > Parameters >
        System Parameters. Default value for delay is 90000ms.
    """,
    'depends': ["base", "web"],
    'js': [
        'static/js/call.js',
    ],
    'data': [
        'data/ir_config_parameter.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
