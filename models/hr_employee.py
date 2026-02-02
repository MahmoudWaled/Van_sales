from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    van_location_id = fields.Many2one(
        'stock.location',
        string='Van location',
        domain=[('usage', '=', 'internal')],
        help='Location representing the van stock.'
    )
