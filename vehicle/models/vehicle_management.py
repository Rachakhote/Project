# -*- coding: utf-8 -*-
import datetime

from datetime import datetime, timedelta
from odoo import models, fields, api


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='Order Number', required=True, track_visibility='onchange', default='NEW', readonly='1')
    user_id = fields.Many2one('res.users', string='User', required=True, track_visibility='onchange',
                              default=lambda self: self.env.company)
    objective = fields.Char(string='Objective', required=True, track_visibility='onchange')
    teacher = fields.Integer(string='Number of Teachers', required=True, track_visibility='onchange')
    student = fields.Integer(string='Number of Students', required=True, track_visibility='onchange')
    model_id = fields.Many2one('fleet.vehicle', string='Model', required=True, track_visibility='onchange')
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='Location', required=True, track_visibility='onchange')
    distance = fields.Float(string='Distance', required=True, track_visibility='onchange')
    budget = fields.Selection([('budget', 'งบประมาณแผ่นดิน'), ('statement', 'งบรายได้'), ('other', 'อื่นๆ')],
                              required=True, track_visibility='onchange')
    start_date = fields.Datetime(string='Start Date', required=True, track_visibility='onchange',
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='End Date', required=True, track_visibility='onchange',
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    driver_id = fields.Many2one('res.users', string='Driver', required=True, track_visibility='onchange')
    # state = fields.Many2one('maintenance', string='State', required=True)

    @api.model
    def create(self, vals):
        new_running_number = self.env['ir.sequence'].next_by_code('vehicle.management.sequence')
        vals['name'] = new_running_number
        record = super(VehicleManagement, self).create(vals)
        return record
