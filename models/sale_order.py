from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'order.sale'

    collection_mode = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('credit', 'Credit'),
    ], string='Collection Mode', default='cash', required=True, tracking=True)
