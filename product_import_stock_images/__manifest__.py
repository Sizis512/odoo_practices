# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Import Stock Product Images',
    "summary": """
    Import main images for your products from a ZIP folder with the stock module.
    """,
    "version": "11.0.1.0.0",
    "author": "Binovo",
    "category": "Web",
    "website": "http://www.binovo.es",
    'depends': ['stock',
                'product_import_images_base'
                ],
    'data': [
        'views/product_import_images_view.xml',
    ],

}
