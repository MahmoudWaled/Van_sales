from odoo import api, models, fields


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
