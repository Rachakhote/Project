# -*- coding: utf-8 -*-
import datetime

from datetime import datetime, timedelta
from odoo import models, fields, api


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='Order Number', tracking=True, default='NEW', readonly=True)
    user_id = fields.Many2one('res.users', string='User', required=True, tracking=True,
                              default=lambda self: self.env.company)
    objective = fields.Char(string='Objective', required=True, tracking=True)
    teacher = fields.Integer(string='Number of Teachers', required=True, tracking=True)
    student = fields.Integer(string='Number of Students', required=True, tracking=True)
    model_id = fields.Many2one('fleet.vehicle', string='Model', required=True, tracking=True)
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='Location', required=True, tracking=True)
    distance = fields.Float(string='Distance', required=True, tracking=True)
    budget = fields.Selection([('budget', 'งบประมาณแผ่นดิน'), ('statement', 'งบรายได้'), ('other', 'อื่นๆ')],
                              required=True, tracking=True)
    start_date = fields.Datetime(string='Start Date', required=True, tracking=True,
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='End Date', required=True, tracking=True,
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    driver_id = fields.Many2one('res.users', string='Driver', required=True, tracking=True)

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             string='Status', default='draft')

    @api.model
    def create(self, vals):
        new_running_number = self.env['ir.sequence'].next_by_code('vehicle.management.sequence')
        vals['name'] = new_running_number
        record = super(VehicleManagement, self).create(vals)
        return record

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

