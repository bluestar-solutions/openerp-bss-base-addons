# -*- coding: utf-8 -*-
# Part of One2Many Action Widget.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'One2Many Action Widget',
    'version': '10.0.2.1',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
One2Many Action Widget
======================

A widget for one2many field which you can customizethe action when a user click
on a line in list.

<field name="my_one2many_ids" widget="one2many_action"
    context="{'on_click_action': 'my_object_method'}">[…]</field>

If on_click_action is not defined, no action will be called on click.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['web'],
    'data': ['views/assets_backend_templates.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
