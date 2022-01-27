# -*- coding: utf-8 -*-
import datetime

from datetime import datetime, timedelta
from odoo import models, fields, api


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='หมายเลข', tracking=True, default='NEW', readonly=True)
    user_id = fields.Many2one('res.users', string='ผู้ขอใช้', readonly=True, tracking=True,
                              default=lambda self: self.env.company)
    position = fields.Char(string='ตำแหน่ง', tracking=True)
    agency = fields.Char(string='หน่วยงาน', tracking=True)
    objective = fields.Char(string='จุดประสงค์ในการขอใช้รถ', tracking=True)
    teacher_number = fields.Integer(string='มีผู้ร่วมเดินทางเป็นอาจารย์', tracking=True)
    student_number = fields.Integer(string='นักศึกษา', tracking=True)
    model_id = fields.Many2one('fleet.vehicle', string='ประเภทรถยนต์', required=True, tracking=True)
    image_128 = fields.Image(related='model_id.image_128', readonly=True)
    location = fields.Text(string='สถานที่', tracking=True)
    distance = fields.Float(string='ระยะทางไป-กลับ', tracking=True)
    budget = fields.Selection(
        [('budget_land', 'งบแผ่นดิน'), ('statements', 'งบรายได้'), ('other', 'งบอื่นๆ')],
        string='งบประมาณค่าน้ำมันเชื้อเพลิง', tracking=True, default='budget_land')
    note = fields.Char(string='ระบุ', tracking=True)
    start_date = fields.Datetime(string='วันเวลาในการออกเดินทาง', tracking=True,
                                 default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    end_date = fields.Datetime(string='วันเวลาในการเดินทางกลับ', tracking=True,
                               default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    responsible = fields.Char(string='ผู้รับผิดชอบควบคุมในการใช้รถยนต์', tracking=True)
    phone_number = fields.Char(string='เบอร์โทรศัพท์', tracking=True)
    office_number = fields.Char(string='เบอร์สำนักงาน', tracking=True)

    # เจ้าหน้าที่ธุรการ

    record = fields.Selection(
        [('approve', 'เห็นควรอนุมัติ'), ('disapproved', 'ไม่เห็นควรอนุมัติ'), ('consider', 'โปรดพิจารณา')],
        string='บันทึก', tracking=True, default='approve')
    driver_id = fields.Many2one('res.users', string='พนักงานขับรถ', tracking=True)
    attendant = fields.Char(string='พนักงานประจำรถ', tracking=True)
    authorities = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True,
                                  default=lambda self: self.env.company)
    approve_date = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # หัวหน้าฝ่ายยานพาหนะ

    propose = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')],
                               string='เสนอ', tracking=True, default='approve')
    because = fields.Char(string='เพราะ', tracking=True)
    department_head = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date01 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # ผู้อำนวยการสำนักงานอธิการบดี

    propose_02 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                  , string='เสนอ', tracking=True, default='approve')
    because_02 = fields.Char(string='เพราะ', tracking=True)
    office_director = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date02 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # รองอธิการบดีฝ่ายบริหาร

    propose_03 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ'), ('consider', 'โปรดพิจารณา')]
                                  , string='เสนอ', tracking=True, default='approve')
    because_03 = fields.Char(string='เพราะ', tracking=True)
    vice_president = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date03 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

    # อธิการบดีมหาวิทยาลัยราชภัฏบุรีรัมย์

    propose_04 = fields.Selection([('approve', 'อนุมัติ'), ('disapproved', 'ไม่อนุมัติ')], string='เสนอ', tracking=True,
                                  default='approve')
    because_04 = fields.Char(string='เพราะ', tracking=True)
    chancellor = fields.Many2one('res.users', string='ลงชื่อ', tracking=True, readonly=True)
    approve_date04 = fields.Date(string='วันที่อนุมัติ', default=fields.Date.today(), readonly=True)

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

    def button_confirm(self):
        for data in self:
            data.write({
                'approve_date': datetime.now().strftime('%Y-%m-%d'),
                'state': 'authorities'
            })
            # ค้นหาข้อมุลจาก Class อื่น
            # obj = self.env['fleet.vehicle']
            # obj.search([เงื่อนไข])
            # obj.xxxxx

            # เขียนข้อมูลทับ
            # obj.write({ชื่อฟิลด์: ค่าที่ต้องการ})

            # ลย
            # obj.unlink(id ของ obj)

            # สร้าง
            # obj = self.env['ชื่อคลาส']
            # newobj = obj.create({ชื่อฟิลด์: ค่าที่ต้องการ})

            # self.approve_date = datetime.now().strftime('%Y-%m-%d')
            # self.state = 'authorities'

    def button_authorities(self):
        self.state = 'department head'

    def button_department(self):
        self.state = 'director'

    def button_director(self):
        self.state = 'vice president'

    def button_president(self):
        self.state = 'chancellor'

    def button_chancellor(self):
        self.state = ''

    def button_cancel(self):
        self.state = 'cancel'
