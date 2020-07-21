# -*- coding: utf-8 -*-
{
    'name': "Gantt view for work orders",
    'version': "0.1",
    'author': '',
    'website': '',
    'category': "Project",
    'summary': "Add gantt view for Manufacturing work orders",
    'description': "",
    'license': 'OPL-1',
    'data': [
        'views/init_data.xml',
        'views/assets.xml',
        'views/workorder_gantt_view.xml',
        'views/workorder_form_view.xml',
    ],
    'depends': ['mrp', 'ba_web_gantt'],
}
