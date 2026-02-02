from odoo import models, fields


class VanRoute(models.Model):
    _name = 'van.route'
    _description = 'Van Sales Route'

    name = fields.Char(string='Route Name', required=True)
    region = fields.Char(string='Region', required=True)
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Scheduled Day')
    partner_ids = fields.Many2many('res.partner', string='Customers')
