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
    position = fields.Char(string='ตำแหน่ง', required=True, tracking=True)
    agency = fields.Char(string='หน่วยงาน', required=True, tracking=True)
    objective = fields.Char(string='วัตถุประสงค์', required=True, tracking=True)
    teacher_number = fields.Integer(string='จำนวนอาจารย์ผู้ร่วมเดินทาง', tracking=True)
    student_number = fields.Integer(string='จำนวนนักศึกษาผู้ร่วมเดินทาง', tracking=True)
    model_id = fields.Many2one('fleet.vehicle', string='Model', required=True, tracking=True)
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='สถานที่', required=True, tracking=True)
    distance = fields.Float(string='ระยะทางไป-กลับ', required=True, tracking=True)
    budget = fields.Selection([('country_budget', 'งบประมาณแผ่นดิน'), ('statements', 'งบรายได้'), ('other', 'อื่นๆ')],
                              string='ค่าน้ำมันเชื้อเพลิง', required=True, tracking=True)
    start_date = fields.Datetime(string='วันเวลาในการออกเดินทาง', tracking=True,
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='วันเวลาในการเดินทางกลับ', tracking=True,
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    responsible_person = fields.Char(string='ผู้รับผิดชอบควบคุมในการใช้รถยนต์', tracking=True)
    phone_number = fields.Char(string='เบอร์โทรศัพท์', tracking=True)
    office_number = fields.Char(string='เบอร์สำนักงาน', tracking=True)

    record = fields.Selection([('approve', 'เห็นควรอนุมัติ'), ('disapproved', 'ไม่เห็นควรอนุมัติ'), ('consider', 'โปรดพิจารณา')],
                              string='บันทึก', required=True, tracking=True)
    driver_id = fields.Many2one('res.users', string='พนักงานขับรถ', tracking=True)
    car_attendant = fields.Char(string='พนักงานประจำรถ', tracking=True)
    administrative_staff = fields.Many2one('res.users', string='ลงชื่อ', required=True, tracking=True)
    approve_date = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    offer = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')],
                             string='เสนอ', required=True, tracking=True)
    reason = fields.Char(string='เพราะ', tracking=True)
    department_head = fields.Many2one('res.users', string='ลงชื่อ', required=True, tracking=True)
    approve_date01 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    offer_part02 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                    , string='เสนอ', required=True, tracking=True)
    reason_part02 = fields.Char(string='เพราะ', tracking=True)
    office_director = fields.Many2one('res.users', string='ลงชื่อ', required=True, tracking=True)
    approve_date02 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    offer_part03 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                    , string='เสนอ', required=True, tracking=True)
    reason_part03 = fields.Char(string='เพราะ', tracking=True)
    vice_president = fields.Many2one('res.users', string='ลงชื่อ', required=True, tracking=True)
    approve_date03 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    offer_part04 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ')], string='เสนอ',
                                    required=True, tracking=True)
    reason_part04 = fields.Char(string='เพราะ', tracking=True)
    chancellor = fields.Many2one('res.users', string='ลงชื่อ', required=True, tracking=True)
    approve_date04 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

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

