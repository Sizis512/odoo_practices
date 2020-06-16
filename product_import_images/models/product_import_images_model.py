from odoo import models, fields, api, exceptions
import zipfile
import random


class ProductImportImages(models.TransientModel):
    _name = 'product.import.images'
    _description = 'Import Product Images'

    products = fields.Many2many(
            'product.template',
            string='Products')
    folder_path = fields.Char("Images folder path")
    new_image = fields.Binary()

    @api.model
    def default_get(self, field_names):
        selected = super(ProductImportImages, self).default_get(field_names)
        selected['products'] = self.env.context['active_ids']
        return selected

    def do_import_images(self):
        self.ensure_one()
        zf = zipfile.ZipFile(self.folder_path)
        name_list = zf.namelist()

        for prod in self.products:
            valid_names = []
            for name in name_list:
                if name[:-4] == prod.default_code:
                    # TODO check if ends in .jpg or .png
                    valid_names.append(name)
            if valid_names:
                image_name = random.choice(valid_names)
                prod.write({'image': zf.read(image_name)})
        return True
