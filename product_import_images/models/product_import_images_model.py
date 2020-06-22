from odoo import models, fields, api, exceptions
import io
import zipfile
import random
import binascii


class ProductImportImages(models.TransientModel):
    _name = 'product.import.images'
    _description = 'Import Product Images'

    products = fields.Many2many(
            'product.template',
            string='Products')
    folder_bin = fields.Binary("Select ZIP folder")
    folder_name = fields.Char()

    def do_import_images(self):
        self.ensure_one()
        if not self.folder_bin:
            raise exceptions.Warning('Select a ZIP folder')
        if not self.folder_name[-4:].lower() == '.zip':
            raise exceptions.Warning('Folder must be ZIP type')
        self.folder_bin = io.BytesIO(binascii.a2b_base64(self.folder_bin))
        zf = zipfile.ZipFile(self.folder_bin)
        name_list = zf.namelist()

        self.products = self.env['product.template'].search([])
        unchanged_images = 0
        for prod in self.products:
            if not prod.default_code:
                unchanged_images += 1
                continue
            valid_names = []
            product_code = prod.default_code.lower()
            i = 0
            while i < len(name_list):
                name = name_list[i]
                name_lower = name_list[i].lower()
                if (name_lower[:-4] == product_code)\
                        and (name_lower.endswith(('.jpg', '.png'))):
                    valid_names.append(name)
                    name_list.remove(name)
                else:
                    i += 1
            if valid_names:
                image_name = random.choice(valid_names)
                image_data = zf.read(image_name)
                image_data = binascii.b2a_base64(image_data)
                prod.write({'image': image_data})
            else:
                unchanged_images += 1
        # TODO popup with import info
        return True

    @api.multi
    def get_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
