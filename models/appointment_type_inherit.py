from odoo import fields, models

class AppointmentType(models.Model):
    _inherit = 'appointment.type'

    stems_max_mb = fields.Integer(string='Límite de tamaño de stems (MB)')
    stems_total_quota_mb = fields.Integer(string='Cuota total de stems (MB)')
