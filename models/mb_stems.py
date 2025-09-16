from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MbStems(models.Model):
    _name = 'mb_dd.stems'
    _description = 'Stems por Evento'
    _order = 'id desc'

    name = fields.Char(required=True, help='Carpeta o alias de stems en el storage')
    calendar_event_id = fields.Many2one('calendar.event', required=True, index=True, ondelete='cascade')
    file_name = fields.Char()
    file_size = fields.Integer(help='Tamaño en bytes')
    content_type = fields.Char()
    object_key = fields.Char(help='Clave/Key en el storage (S3/R2/etc.)')
    uploaded_by_id = fields.Many2one('res.partner', string='Subido por')
    note = fields.Text()

    def _effective_limits(self):
        ICP = self.env['ir.config_parameter'].sudo()
        max_file_mb = int(ICP.get_param('mb_dd.stems_max_mb', '100') or 100)
        total_mb = int(ICP.get_param('mb_dd.stems_total_quota_mb', '2000') or 2000)
        return max_file_mb, total_mb

    def check_quota_before_upload(self, size_bytes):
        max_file_mb, total_mb = self._effective_limits()
        if size_bytes > max_file_mb * 1024 * 1024:
            raise UserError(_('Archivo excede el límite por archivo (%s MB).') % max_file_mb)
        total_used = sum(self.search([('calendar_event_id', '=', self.calendar_event_id.id)]).mapped('file_size') or [0])
        if (total_used + size_bytes) > total_mb * 1024 * 1024:
            raise UserError(_('Se excede la cuota total de stems para este evento (%s MB).') % total_mb)
