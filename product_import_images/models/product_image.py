from odoo import fields, models


class ProductImage(models.Model):
    _inherit = 'product.image'
    filename = fields.Char('File Name')
