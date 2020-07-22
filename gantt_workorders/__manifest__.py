# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Gantt view for work orders',
    'summary': """
    Add gantt view for Manufacturing work orders
    """,
    'version': '11.0.1.0.0',
    'author': 'Binovo',
    'category': 'Project',
    'website': 'http://www.binovo.es',
    'depends': ['mrp', 'ba_web_gantt'],
    'data': [
        'views/init_data.xml',
        'views/assets.xml',
        'views/workorder_gantt_view.xml',
        'views/workorder_form_view.xml',
    ],
    'qweb': [
        'static/src/xml/template.xml',
    ],
}
