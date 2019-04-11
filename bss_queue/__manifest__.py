# -*- coding: utf-8 -*-
# Part of Jobs Queue.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Jobs Queue',
    'version': '10.0.2.0',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Jobs Queue
==========

A jobs queue system.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_cron_data.xml',

        'views/bss_queue_views.xml',
        'views/bss_queue_step_views.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
