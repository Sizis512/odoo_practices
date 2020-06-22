from odoo import models, fields, api, exceptions
import io
import zipfile
import random
import binascii
from PIL import Image


class ProductImportImages(models.TransientModel):
    _name = 'product.import.images'
    _description = 'Import Product Images'

    products = fields.Many2many(
            'product.template',
            string='Products')
    folder_bin = fields.Binary("Select ZIP folder")

    @api.model
    def default_get(self, field_names):
        selected = super(ProductImportImages, self).default_get(field_names)
        selected['products'] = self.env.context['active_ids']
        return selected

    def do_import_images(self):
        # self.ensure_one()

        self.folder_bin = io.BytesIO(binascii.a2b_base64(self.folder_bin))
        zf = zipfile.ZipFile(self.folder_bin)
        name_list = zf.namelist()

        not_found_names = []
        for prod in self.products:
            valid_names = []
            product_code = prod.default_code.lower()
            for name in name_list:
                name_lower = name.lower()
                if name_lower[:-4] == product_code:
                    if name_lower.endswith(('.jpg'.lower(), '.png'.lower())):
                        valid_names.append(name)
                        name_list.remove(name)
            if valid_names:
                #import pudb; pudb.set_trace()
                image_name = random.choice(valid_names)
                image_data = zf.read(image_name)
                image_data = binascii.b2a_base64(image_data)
                prod.write({'image': image_data})
            else:
                not_found_names.append(prod.name)
        # TODO popup with import info
        return True

    @api.multi
    def get_view(self):
        view_id = self.env.ref('product_import_images.Import Product Images').id
        return {
            'name': 'Import Images',
            'view_type': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'product.import.images',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
        }