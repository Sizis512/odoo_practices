from odoo import models, fields, api, exceptions
import io
import os
import zipfile
import base64


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
        if not self.folder_name.lower().endswith('.zip'):
            raise exceptions.Warning('Folder must be ZIP type')
        self.folder_bin = io.BytesIO(base64.b64decode(self.folder_bin))
        zf = zipfile.ZipFile(self.folder_bin)
        name_list = zf.namelist()

        self.products = self.env['product.template'].search([])
        unchanged_images = 0
        for prod in self.products:
            if not prod.default_code:
                unchanged_images += 1
                continue
            valid_images = []
            product_code = prod.default_code.lower()
            i = 0
            while i < len(name_list):
                name = name_list[i]
                name_lower = name_list[i].lower()
                if (os.path.splitext(name_lower)[0].rsplit('-', 1)[0] == product_code)\
                        and (name_lower.endswith(('.jpg', '.png'))):
                    valid_images.append(name)
                    name_list.remove(name)
                else:
                    i += 1
            if valid_images:
                valid_images.sort(key=len)
                main_image = zf.read(valid_images[0])
                main_image_b64 = base64.b64encode(main_image)
                update_dict = {'image': main_image_b64}
                product_image_list = []
                #self.env['product.image'].search([('name', '=', prod.default_code)]).unlink()
                for image in valid_images:
                    if not self.env['product.image'].search([('filename', '=', image[:-4])]):
                        product_image_dict = {'name': prod.default_code,
                                              'image': base64.b64encode(zf.read(image)),
                                              'filename': image[:-4],
                                              'product_tmpl_id': prod.id}
                        product_image_list.append([0, 0, product_image_dict])
                update_dict['product_image_ids'] = product_image_list
                prod.write(update_dict)
            else:
                unchanged_images += 1
        # TODO popup with import info
        return True
