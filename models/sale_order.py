from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.tools import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    collection_mode = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('credit', 'Credit'),
    ], string='Collection Mode', default='cash', required=True, tracking=True)

    allowed_partners_ids = fields.Many2many(
        'res.partner', compute='_compute_allowed_partners')

    @api.depends('user_id')
    def _compute_allowed_partners(self):
        for order in self:
            user = order.user_id or self.env.user
            current_day = fields.Date.context_today(self)
            current_day_index = str(current_day.weekday())
            route = self.env['van.route'].search([
                ('user_id', '=', user.id),
                ('day_of_week', '=', current_day_index)
            ], limit=1)
            if route:
                order.allowed_partners_ids = route.partner_ids
            else:
                order.allowed_partners_ids = self.env['res.partner'].search([
                ])

    def action_confirm(self):
        print('****** from action_confirm method ******')
        # validation: check if the van is empty or products less than ordered qty
        for order in self:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', order.user_id.id)], limit=1)
            if employee and employee.van_location_id:
                van_location = employee.van_location_id
                print(f"***** Van Location: {van_location.name} *****")
                for line in order.order_line:
                    print(
                        f"***** Checking product: {line.product_id.name} *****")
                    if line.product_id.type == 'consu':
                        van_qty_available = line.product_id.with_context(
                            location=van_location.id).qty_available
                        print(
                            f"***** Product: {line.product_id.name}, Van Qty Available: {van_qty_available}, Ordered Qty: {line.product_uom_qty} *****")
                        if van_qty_available < line.product_uom_qty:
                            print('***** Raising UserError for stock shortage *****')
                            raise UserError(_(
                                f"Stock shortage in your van for product: ({line.product_id.name})\n"
                                f"Current Stock: {van_qty_available}\n"
                                f"Requested Quantity: {line.product_uom_qty}"
                            ))

        res = super(SaleOrder, self).action_confirm()
        print('****** after super in action_confirm method ******')
        # Modification: change picking location to van location and move location to van location
        for order in self:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', order.user_id.id)], limit=1)
            if employee and employee.van_location_id:
                for picking in order.picking_ids:
                    picking.location_id = employee.van_location_id.id
                    print(
                        f"***** Updated picking location to van location: {employee.van_location_id.name} *****")
                    for move in picking.move_ids:
                        move.location_id = employee.van_location_id.id
                        print(
                            f"***** Updated move location to van location: {employee.van_location_id.name} *****")

        return res
