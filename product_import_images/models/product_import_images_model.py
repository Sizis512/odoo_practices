from odoo import models, fields, api, exceptions, _
import io
import os
import zipfile
import base64


class ProductImportImages(models.Model):
    _name = 'product.import.images'
    _description = 'Import Product Images'
    _auto = False

    file_bin = fields.Binary("Select ZIP file", required=True)
    file_name = fields.Char("Filename", required=True)
    popup_message = fields.Char("Pop-up Message", readonly=True)

    @api.multi
    def do_import_images(self):
        self.ensure_one()
        if not self.file_name.lower().endswith('.zip'):
            raise exceptions.Warning(_('File must be ZIP type'))
        self.file_bin = io.BytesIO(base64.b64decode(self.file_bin))
        zf = zipfile.ZipFile(self.file_bin)
        name_list = zf.namelist()

        products = self.env['product.template'].search([])
        total_imported_images = 0
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
                if (os.path.splitext(name_lower)[0].rsplit('-', 1)[0]
                    == product_code) \
                        and (name_lower.endswith(('.jpg', '.png'))):
                    valid_images.append(name)
                    name_list.remove(name)
                else:
                    i += 1
            if valid_images:
                valid_images.sort(key=len)
                update_dict = {}
                has_main = self.env['product.template']\
                    .search([('default_code', '=', prod.default_code)]).image
                if not has_main:
                    main_image = zf.read(valid_images[0])
                    main_image_b64 = base64.b64encode(main_image)
                    update_dict['image'] = main_image_b64
                product_image_list = []
                for image in valid_images:
                    same_image = self.env['product.image'] \
                            .search([('filename', '=', image[:-4])])
                    if same_image:
                        same_image.unlink()
                    new_image = base64.b64encode(zf.read(image))
                    product_image_dict = {'name': prod.default_code,
                                          'image': new_image,
                                          'filename': image[:-4],
                                          'product_tmpl_id': prod.id}
                    product_image_list.append([0, 0, product_image_dict])
                    total_imported_images += 1
                update_dict['product_image_ids'] = product_image_list
                prod.write(update_dict)
                total_products_changed += 1
        message = (_("Successfully imported ")
                   + str(total_imported_images)
                   + _(" images into ")
                   + str(total_products_changed)
                   + _(" products.")
                   )
        self.write({'popup_message': message})
        popup_view_id = self.env.ref("product_import_images.popup_message_view").id
        return {
            'name': 'Info',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.import.images',
            'res_id': self.id,
            'views': [(popup_view_id, 'form')],
            'target': 'new',
        }
