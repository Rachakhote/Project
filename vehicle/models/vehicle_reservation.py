# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class VehicleReservation(models.Model):
    _name = 'vehicle.reservation'
    _description = 'Vehicle Reservation System'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='Number', tracking=True, default='NEW', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True, tracking=True,
                              default=lambda self: self.env.company)
    position = fields.Char(string='ตำแหน่ง', tracking=True)
    agency = fields.Char(string='หน่วยงาน', tracking=True)
    objective = fields.Char(string='วัตถุประสงค์ในการขอใช้รถ', tracking=True)
    teacher_n = fields.Integer(string='มีผู้ร่วมเดินทางเป็นอาจารย์', tracking=True)
    student_n = fields.Integer(string='นักศึกษา', tracking=True)
    model_id = fields.Many2one('fleet.vehicle', string='ประเภทรถยนต์', tracking=True)
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='สถานที่', tracking=True)
    distance = fields.Float(string='ระยะทางไป-กลับ', tracking=True)
    budget = fields.Selection(
        [('land', 'งบแผ่นดิน'), ('income', 'งบรายได้'), ('other', 'งบอื่นๆ')],
        string='งบประมาณค่าน้ำมันเชื้อเพลิง', tracking=True, default='land')
    specify = fields.Char(string='ระบุ', tracking=True)
    start_date = fields.Datetime(string='วันเวลาในการออกเดินทาง', tracking=True,
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='วันเวลาในการเดินทางกลับ', tracking=True,
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    responsible = fields.Char(string='ผู้รับผิดชอบควบคุมในการใช้รถยนต์', tracking=True)
    phone_number = fields.Char(string='เบอร์โทรศัพท์', tracking=True)
    office_number = fields.Char(string='เบอร์สำนักงาน', tracking=True)

    # เจ้าหน้าที่
    record = fields.Selection(
        [('approve', 'เห็นควรอนุมัติ'), ('disapproved', 'ไม่เห็นควรอนุมัติ'), ('consider', 'โปรดพิจารณา')],
        string='บันทึก', tracking=True, default='approve')
    driver_id = fields.Many2one('res.users', string='พนักงานขับรถ', tracking=True)
    attendant = fields.Char(string='พนักงานประจำรถ', tracking=True)
    authorities = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True,
                                  default=lambda self: self.env.company)
    approve_date = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # หัวหน้าฝ่าย
    propose = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')],
                               string='เสนอ', tracking=True, default='approve')
    because = fields.Char(string='เพราะ', tracking=True)
    head = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date_head = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # ผู้อำนวยการ
    propose_director = fields.Selection(
        [('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
        , string='เสนอ', tracking=True, default='approve')
    because_director = fields.Char(string='เพราะ', tracking=True)
    director = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date_director = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # รองอธิการ
    propose_secondary = fields.Selection(
        [('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
        , string='เสนอ', tracking=True, default='approve')
    because_secondary = fields.Char(string='เพราะ', tracking=True)
    president = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date_secondary = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # อธิการบดี
    propose_chancellor = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ')],
                                          string='เสนอ', tracking=True, default='approve')
    because_chancellor = fields.Char(string='เพราะ', tracking=True)
    chancellor = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date_chancellor = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    state = fields.Selection(
        [('draft', 'ฉบับร่าง'), ('authorities', 'เจ้าหน้าที่'), ('department', 'หัวหน้าฝ่าย'),
         ('director', 'ผู้อำนวยการ'), ('president', 'รองอธิการบดี'),
         ('chancellor', 'อธิการบดี'), ('cancel', 'ยกเลิก')],
        string='สถานะ', default='draft')

    @api.model
    def create(self, vals):
        new_running_number = self.env['ir.sequence'].next_by_code('vehicle.reservation.sequence')
        vals['name'] = new_running_number
        record = super(VehicleReservation, self).create(vals)
        return record

    def button_confirm(self):
        for data in self:
            data.write({
                'approve_date': datetime.now().strftime('%Y-%m-%d'),
                'state': 'authorities'
            })

    def button_authorities(self):
        self.state = 'department'

    def button_department(self):
        self.state = 'director'

    def button_director(self):
        self.state = 'president'

    def button_president(self):
        self.state = 'chancellor'

    def button_chancellor(self):
        self.state = ''

    def button_cancel(self):
        self.state = 'cancel'
