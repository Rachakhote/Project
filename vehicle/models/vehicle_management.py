# -*- coding: utf-8 -*-
import datetime

from datetime import datetime, timedelta
from odoo import models, fields


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='Order Number', track_visibility='onchange')
    partner_id = fields.Many2one('fleet.vehicle', string='Model', required=True, track_visibility='onchange')
    driver_id = fields.Many2one('res.users', string='Driver', required=True, track_visibility='onchange')
    objective = fields.Char(string='Objective', required=True, track_visibility='onchange')
    location = fields.Text(string='Location', required=True, track_visibility='onchange')
    distance = fields.Float(string='Distance', required=True, track_visibility='onchange')
    travel_date = fields.Datetime(string='Travel Date', required=True, track_visibility='onchange',
                                  default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    return_date = fields.Datetime(string='Return Date', required=True, track_visibility='onchange',
                                  default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    oil_budget = fields.Selection([('country_budget', 'งบประมาณแผ่นดิน'),
                                   ('income_statement', 'งบรายได้'),
                                   ('other', 'อื่นๆ')], required=True, track_visibility='onchange')
    n_teacher = fields.Integer(string='Teachers Number', required=True, track_visibility='onchange')
    n_student = fields.Integer(string='Students Number', required=True, track_visibility='onchange')
    note = fields.Text(string='Description', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='User', required=True, track_visibility='onchange',
                              default=lambda self: self.env.company)

    # state_id = fields.Many2one('maintenance', string='State', required=True)


