from odoo import models, fields, api


class ProductImportImages(models.TransientModel):
    _name = 'product.import.images'
    _description = 'Import Product Images'

    folder_path = fields.Char()
