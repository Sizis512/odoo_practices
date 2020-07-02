# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions, _
import io
import os
import zipfile
import base64


class ProductImportStockImages(models.TransientModel):
    _inherit = 'product.import.images.base'

    @api.multi
    def do_import_stock_images(self):
        self.ensure_one()
        if not self.file_name.lower().endswith('.zip'):
            raise exceptions.Warning(_('File must be ZIP type'))
        self.file_bin = io.BytesIO(base64.b64decode(self.file_bin))
        zf = zipfile.ZipFile(self.file_bin)
        name_list = zf.namelist()

        products = self.env['product.template'].search([])
        total_products_changed = 0
        for prod in products:
            if not prod.default_code:
                continue
            valid_images = []
            product_code = prod.default_code.lower()
            i = 0
            while i < len(name_list):
                name = name_list[i]
                name_lower = name_list[i].lower()
                if (os.path.splitext(name_lower)[0] == product_code) \
                        and (name_lower.endswith(('.jpg', '.png', '.jpeg'))):
                    valid_images.append(name)
                    name_list.remove(name)
                else:
                    i += 1
            if valid_images:
                main_image = zf.read(valid_images[0])
                main_image_b64 = base64.b64encode(main_image)
                prod.write({'image': main_image_b64})
                total_products_changed += 1
        message = (_("Successfully changed the image of ")
                   + str(total_products_changed)
                   + _(" products.")
                   )
        self.write({'popup_message': message})
        popup_view_id = self.env.ref("product_import_stock_images.popup_message_view").id
        return {
            'name': 'Info',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.import.images.base',
            'res_id': self.id,
            'views': [(popup_view_id, 'form')],
            'target': 'new',
        }
