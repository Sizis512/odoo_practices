# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProductImportImages(models.TransientModel):
    _name = 'product.import.images.base'
    _description = 'Import Product Images'

    file_bin = fields.Binary("Select ZIP file", required=True)
    file_name = fields.Char("Filename", required=True)
    popup_message = fields.Char("Pop-up Message", readonly=True)
