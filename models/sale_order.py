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
        # validation: check if the van is empty or products less than ordered qty
        for order in self:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', order.user_id.id)], limit=1)
            if employee and employee.van_location_id:
                van_location = employee.van_location_id
                for line in order.order_line:
                    if line.product_id.type == 'consu':
                        van_qty_available = line.product_id.with_context(
                            location=van_location.id).qty_available
                        if van_qty_available < line.product_uom_qty:
                            raise UserError(_(
                                f"Stock shortage in your van for product: ({line.product_id.name})\n"
                                f"Current Stock: {van_qty_available}\n"
                                f"Requested Quantity: {line.product_uom_qty}"
                            ))

        res = super(SaleOrder, self).action_confirm()
        # Modification & Automation: change picking location to van location and move location to van location
        #   then automate validating picking , creating & posting invoice and create the payment if collection is cash
        for order in self:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', order.user_id.id)], limit=1)
            if employee and employee.van_location_id:
                van_location = employee.van_location_id
                for picking in order.picking_ids:
                    picking.location_id = van_location.id
                    for move in picking.move_ids:
                        move.location_id = van_location.id
                        move.quantity = move.product_uom_qty
                    # validate picking
                    picking.with_context(skip_backorder=True).button_validate()
                # create & post invoice
                if order.invoice_status == 'to invoice':
                    invoice = order._create_invoices()
                    invoice.action_post()
                    # create payment if collection mode is cash
                    if order.collection_mode == 'cash':
                        journal = self.env['account.journal'].search(
                            [('type', '=', 'cash')], limit=1)
                        if journal:
                            self.env['account.payment.register'].with_context(
                                active_model='account.move',
                                active_ids=invoice.ids,).create({
                                    'journal_id': journal.id,
                                })._create_payments()
        return res
