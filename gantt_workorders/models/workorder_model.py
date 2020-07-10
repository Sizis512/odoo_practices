# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WorkOrdersModel(models.Model):
    _inherit = 'mrp.workorder'

    progress = fields.Integer(compute='_compute_progress')
    parent_id = fields.Many2one(comodel_name='mrp.workorder',
                                string='Parent Work Order')
    user_id = fields.Many2one(comodel_name='res.users',
                              string='Responsible')

    @api.one
    @api.depends('duration_percent')
    def _compute_progress(self):
        self.progress = 100 - self.duration_percent

    @api.onchange('parent_id')
    def _change_next_work_order_id(self):
        #TODO
        return