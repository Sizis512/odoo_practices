from odoo import fields, models, exceptions


class ProductImage(models.Model):
    _inherit = 'product.image'
    filename = fields.Char('File Name')
