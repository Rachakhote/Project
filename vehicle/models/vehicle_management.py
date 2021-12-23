# -*- coding: utf-8 -*-


from odoo import models, fields


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'

    name = fields.Char(string='Order Number')
    partner_id = fields.Many2one('fleet.vehicle', string='Model', required=True)
    driver_id = fields.Many2one('res.users', string='Driver', required=True)
    objective = fields.Char(string='Objective', required=True)
    location = fields.Text(string='Location', required=True)
    distance = fields.Float(string='Distance', required=True)
    travel_date = fields.Datetime(string='Travel Date', required=True)
    return_date = fields.Datetime(string='Return Date', required=True)
    oil_budget = fields.Selection([('country_budget', 'งบประมาณแผ่นดิน'),
                                   ('income_statement', 'งบรายได้'),
                                   ('other', 'อื่นๆ')], required=True)
    n_teacher = fields.Integer(string='Teachers Number', required=True)
    n_student = fields.Integer(string='Students Number', required=True)
    note = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User', required=True)

    # state_id = fields.Many2one('maintenance', string='State', required=True)


