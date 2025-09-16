from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    mb_stems_count = fields.Integer(compute='_compute_mb_stems_count', string='Stems')

    def _compute_mb_stems_count(self):
        Stems = self.env['mb_dd.stems']
        for ev in self:
            ev.mb_stems_count = Stems.search_count([('calendar_event_id', '=', ev.id)])

    def action_mb_open_stems(self):
        self.ensure_one()
        action = self.env.ref('mb_digital_downloads.action_mb_dd_stems').read()[0]
        action['domain'] = [('calendar_event_id', '=', self.id)]
        action['context'] = {'default_calendar_event_id': self.id}
        return action

    def action_create_google_meet(self):
        raise UserError(_('Configura Google API en parámetros mb_dd.* y reemplaza este placeholder.'))
