# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, exceptions


class ProductImage(models.Model):
    _inherit = 'product.image'
    filename = fields.Char('File Name')
