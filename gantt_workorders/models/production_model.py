# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductionsModel(models.Model):
    _inherit = 'mrp.production'

    def button_plan(self):
        ret = super(ProductionsModel, self).button_plan()
        for rec in self.env['mrp.workorder'].search([('production_id', '=', self.id)]):
            rec.parent_id = rec.search([('next_work_order_id', '=', rec.id)])
            rec.user_id = rec.production_id.user_id
        return ret
