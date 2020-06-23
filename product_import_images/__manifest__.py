{
    'name': 'Import Product Images',
    'description': 'Import images for your products from a ZIP folder',
    'author': 'Guillermo Murcia',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_import_images_view.xml',
    ],
}
