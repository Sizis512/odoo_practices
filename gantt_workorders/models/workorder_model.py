# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, exceptions, _


class WorkOrdersModel(models.Model):
    _inherit = 'mrp.workorder'

    progress = fields.Integer(compute='_compute_progress')
    parent_id = fields.Many2one(comodel_name='mrp.workorder',
                                string='Parent Work Order')
    user_id = fields.Many2one(comodel_name='res.users',
                              string='Responsible')

    @api.model
    def init_data(self):
        for rec in self.search([]):
            rec.parent_id = rec.search([('next_work_order_id', '=', rec.id)])
            rec.user_id = rec.production_id.user_id

    @api.one
    @api.depends('duration_percent')
    def _compute_progress(self):
        self.progress = 100 - self.duration_percent

    def _parent_write(self, parent_id):
        old_parent = self.parent_id
        if old_parent:
            old_parent.next_work_order_id = False
        super().write({'parent_id': parent_id})
        if self.parent_id:
            new_parents_old_child = self.parent_id.next_work_order_id
            if new_parents_old_child and new_parents_old_child != self:
                new_parents_old_child.parent_id = False
            self.parent_id.next_work_order_id = self
        return True

    @api.multi
    def write(self, values):
        if 'parent_id' in values:
            parent_id = values['parent_id']
            del values['parent_id']
            super().write(values)
            for rec in self:
                rec._parent_write(parent_id)
            return True
        else:
            return super().write(values)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for workorder in self:
            if not workorder._check_recursion():
                raise exceptions.ValidationError(_('Error! You cannot create recursive hierarchy of work order(s).'))
