# -*- coding: utf-8 -*-
# © 2020 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTodo(TransactionCase):

    def test_create_workorder(self):
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Product',
            'uom_id': self.env.ref('product.product_uom_unit').id
        })
        product = self.env['product.product'].create({
            'name': 'Test Product',
            'uom_id': self.env.ref('product.product_uom_unit').id
        })
        workcenter = self.env['mrp.workcenter'].create({
            'name': 'Test Workcenter'
        })
        routing = self.env['mrp.routing'].create({
            'name': 'Test Routing'
        })
        operation1 = self.env['mrp.routing.workcenter'].create({
            'name': 'operation1',
            'workcenter_id': workcenter.id,
            'routing_id': routing.id,
            'sequence': 1
        })
        operation2 = self.env['mrp.routing.workcenter'].create({
            'name': 'operation2',
            'workcenter_id': workcenter.id,
            'routing_id': routing.id,
            'sequence': 2
        })
        operation3 = self.env['mrp.routing.workcenter'].create({
            'name': 'operation3',
            'workcenter_id': workcenter.id,
            'routing_id': routing.id,
            'sequence': 3
        })
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product_tmpl.id,
            'routing_id': routing.id
        })
        production = self.env['mrp.production'].create({
            'product_id': product.id,
            'product_qty': 1.0,
            'bom_id': bom.id,
            'product_uom_id': product.uom_id.id
        })

        production.button_plan()
        workorders = production.workorder_ids.sorted(key=lambda r: r.id)

        self.assertFalse(workorders[0].parent_id)
        self.assertEqual(workorders[0].user_id, production.user_id)
        self.assertEqual(workorders[1].parent_id, workorders[0])
        self.assertEqual(workorders[1].user_id, production.user_id)
        self.assertEqual(workorders[2].parent_id, workorders[1])
        self.assertEqual(workorders[2].user_id, production.user_id)

        return workorders

    def test_recursive_hierarchy(self):
        workorders = self.test_create_workorder()

        with self.assertRaises(ValidationError):
            workorders[0].write({'parent_id': workorders[2].id})

    def test_change_parent(self):
        workorders = self.test_create_workorder()
        workorders[2].write({'parent_id': workorders[0].id})

        self.assertEqual(workorders[0].next_work_order_id, workorders[2])
        self.assertEqual(workorders[2].parent_id, workorders[0])
        self.assertFalse(workorders[1].parent_id)
        self.assertFalse(workorders[1].next_work_order_id)

    def test_remove_parent(self):
        workorders = self.test_create_workorder()
        workorders[1].write({'parent_id': False})

        self.assertFalse(workorders[1].parent_id)
        self.assertFalse(workorders[0].next_work_order_id)

    def test_change_start_end_times(self):
        workorders = self.test_create_workorder()
        workorders.write({
            'date_planned_start': '2020-07-22 16:00:00',
            'date_planned_finished': '2020-07-24 16:00:00'
        })

        self.assertEqual(workorders[0].date_planned_start, '2020-07-22 16:00:00')
        self.assertEqual(workorders[0].date_planned_finished, '2020-07-24 16:00:00')

    def test_progress(self):
        workorders = self.test_create_workorder()
        workorders[0].write({'duration_percent': 75})

        self.assertEqual(workorders[0].progress, 25)

    def test_change_multi_parent(self):
        workorders = self.test_create_workorder()
        self.test_remove_parent()
        workorders[1:].write({'parent_id': workorders[0].id})

        self.assertEqual(workorders[0].next_work_order_id, workorders[2])
        self.assertEqual(workorders[2].parent_id, workorders[0])
        self.assertFalse(workorders[1].parent_id)
        self.assertFalse(workorders[1].next_work_order_id)
