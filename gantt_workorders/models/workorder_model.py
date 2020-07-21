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
    # descendants = fields.One2many('mrp.workorder', 'parent_id', compute='_compute_descendants', store=True)

    @api.model
    def init_data(self):
        for rec in self.search([]):
            print(self.name)
            rec.long_name = ("%s - %s - %s" % (rec.production_id.name, rec.product_id.name, rec.name))
            rec.parent_id = rec.search([('next_work_order_id', '=', rec.id)])
            rec.user_id = rec.production_id.user_id

    @api.one
    @api.depends('duration_percent')
    def _compute_progress(self):
        self.progress = 100 - self.duration_percent

    @api.multi
    def write(self, values):
        if self._name == 'mrp.workorder' and 'parent_id' in values:
            old_parent = self.parent_id
            if old_parent:
                old_parent.next_work_order_id = False
            super(WorkOrdersModel, self).write(values)
            if self.parent_id:
                new_parents_old_child = self.parent_id.next_work_order_id
                if new_parents_old_child and new_parents_old_child != self:
                    new_parents_old_child.parent_id = False
                self.parent_id.next_work_order_id = self
            return True
        else:
            return super(WorkOrdersModel, self).write(values)

    # @api.depends('next_work_order_id', 'next_work_order_id.descendants')
    # def _compute_descendants(self):
    #     if not self.next_work_order_id:
    #         self.write({'descendants': [5, 0, 0]})
    #     else:
    #         if self.next_work_order_id.descendants:
    #             self.write({'descendants': [6, 0, self.next_work_order_id.descendants]})
    #         self.write({'descendants': [4, self.next_work_order_id, 0]})

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for workorder in self:
            if not workorder._check_recursion():
                raise exceptions.ValidationError(_('Error! You cannot create recursive hierarchy of work order(s).'))
