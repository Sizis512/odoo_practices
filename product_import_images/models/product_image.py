from odoo import fields, models
import random


class ProductImage(models.Model):
    _inherit = 'product.image'
    filename = fields.Char('File Name')

    def do_change_main_image(self):
        new_main = self.image
        product = self.env['product.template'].search([('default_code', '=', self.name)])
        product.write({'image': new_main})
        return True

    def do_delete_image(self):
        self.search([('filename', '=', self.filename)]).unlink()
        return True
