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
    position = fields.Char(string='ตำแหน่ง', tracking=True)
    agency = fields.Char(string='หน่วยงาน', tracking=True)
    objective = fields.Char(string='วัตถุประสงค์', tracking=True)
    teacher_number = fields.Integer(string='จำนวนอาจารย์ผู้ร่วมเดินทาง', tracking=True)
    student_number = fields.Integer(string='จำนวนนักศึกษาผู้ร่วมเดินทาง', tracking=True)
    model_id = fields.Many2one('fleet.vehicle', string='Model', required=True, tracking=True)
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='สถานที่', tracking=True)
    distance = fields.Float(string='ระยะทางไป-กลับ', tracking=True)
    budget = fields.Selection([('country_budget', 'งบประมาณแผ่นดิน'), ('statements', 'งบรายได้'), ('other', 'อื่นๆ')],
                              string='ค่าน้ำมันเชื้อเพลิง', tracking=True)
    start_date = fields.Datetime(string='วันเวลาในการออกเดินทาง', tracking=True,
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='วันเวลาในการเดินทางกลับ', tracking=True,
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    responsible = fields.Char(string='ผู้รับผิดชอบควบคุมในการใช้รถยนต์', tracking=True)
    phone_number = fields.Char(string='เบอร์โทรศัพท์', tracking=True)
    office_number = fields.Char(string='เบอร์สำนักงาน', tracking=True)

    record = fields.Selection(
        [('approve', 'เห็นควรอนุมัติ'), ('disapproved', 'ไม่เห็นควรอนุมัติ'), ('consider', 'โปรดพิจารณา')],
        string='บันทึก', tracking=True)
    driver_id = fields.Many2one('res.users', string='พนักงานขับรถ', tracking=True)
    attendant = fields.Char(string='พนักงานประจำรถ', tracking=True)
    authorities = fields.Many2one('res.users', string='ลงชื่อ', tracking=True)
    approve_date = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    propose = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')],
                               string='เสนอ', tracking=True)
    because = fields.Char(string='เพราะ', tracking=True)
    department_head = fields.Many2one('res.users', string='ลงชื่อ', tracking=True)
    approve_date01 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    propose_02 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                  , string='เสนอ', tracking=True)
    because_02 = fields.Char(string='เพราะ', tracking=True)
    office_director = fields.Many2one('res.users', string='ลงชื่อ', tracking=True)
    approve_date02 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    propose_03 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                  , string='เสนอ', tracking=True)
    because_03 = fields.Char(string='เพราะ', tracking=True)
    vice_president = fields.Many2one('res.users', string='ลงชื่อ', tracking=True)
    approve_date03 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    propose_04 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ')], string='เสนอ', tracking=True)
    because_04 = fields.Char(string='เพราะ', tracking=True)
    chancellor = fields.Many2one('res.users', string='ลงชื่อ', tracking=True)
    approve_date04 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), tracking=True)

    state = fields.Selection(
        [('draft', 'ฉบับร่าง'), ('authorities', 'เจ้าหน้าที่'), ('department head', 'หัวหน้าฝ่าย'),
         ('director', 'ผู้อำนวยการ'), ('vice president', 'รองอธิการบดี'),
         ('chancellor', 'อธิการบดี'), ('cancel', 'ยกเลิก')],
        string='สถานะ', default='draft')

    @api.model
    def create(self, vals):
        new_running_number = self.env['ir.sequence'].next_by_code('vehicle.management.sequence')
        vals['name'] = new_running_number
        record = super(VehicleManagement, self).create(vals)
        return record

    def action_authorities(self):
        self.state = 'authorities'

    # def action_department(self):
    #     self.state = 'department head'
    #
    # def action_draft(self):
    #     self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
