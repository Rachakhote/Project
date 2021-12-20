# -*- coding: utf-8 -*-

from odoo import models, fields


class VehicleManagement(models.Model):
    _name = 'vehicle.management'
    _description = 'Vehicle Management'

    name = fields.Char(string='Model', required=True)
    license_plate = fields.Char(string='License Plate', required=True)
    note = fields.Text(string='Description')
