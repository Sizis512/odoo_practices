from odoo import models, fields, api, exceptions
import logging
import zipfile
import random
import binascii
from tkinter.filedialog import askdirectory

_logger = logging.getLogger(__name__)

class ProductImportImages(models.TransientModel):
    _name = 'product.import.images'
    _description = 'Import Product Images'

    products = fields.Many2many(
            'product.template',
            string='Products')
    folder_path = fields.Char("Images folder path",
                              default='/home/sizis/odoo-dev/practice_addons/product_import_images/new_images.zip')
    new_image = fields.Binary()

    @api.model
    def default_get(self, field_names):
        selected = super(ProductImportImages, self).default_get(field_names)
        selected['products'] = self.env.context['active_ids']
        return selected

    def do_import_images(self):
        # self.ensure_one()
        if not self.folder_path or self.folder_path[-4:] != '.zip':
            raise exceptions.Warning('Invalid folder path!')
        zf = zipfile.ZipFile(self.folder_path)
        name_list = zf.namelist()
        not_found_names = []

        for prod in self.products:
            valid_names = []
            product_code = prod.default_code.lower()
            for name in name_list:
                if name[:-4].lower() == product_code:
                    if name.lower().endswith(('.jpg'.lower(), '.png'.lower())):
                        valid_names.append(name)
            if valid_names:
                image_name = random.choice(valid_names)
                bytes_data = zf.read(image_name)
                base64_data = binascii.b2a_base64(bytes_data)
                prod.write({'image': base64_data})
            else:
                not_found_names.append(prod.name)
        # TODO popup with the not found images
        return True
