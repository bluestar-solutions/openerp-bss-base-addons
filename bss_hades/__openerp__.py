# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
    'name': 'HADES - Helpful Analytical Data Extraction System',
    'version': 'master',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Helpful Analytical Data Extraction System
=========================================

TODO
    """,
    'author': u'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [
        'bss_parameters',
    ],
    'demo': [],
    'data': [
        "module_menu.xml",
        "request_type_view.xml",
        "request_data_view.xml",
        "request_parameter_view.xml",

        "wizard/download_wizard_view.xml",

        "security/security_groups.xml",
        "security/ir.model.access.csv",
    ],
    'css': ['static/src/css/style.css'],
    'js': ['static/src/js/request_view.js'],
    'qweb': ['static/src/xml/web_request_view.xml'],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
