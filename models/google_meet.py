from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta
import json
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except Exception:
    service_account = build = None

class AppointmentBooking(models.Model):
    _inherit = 'appointment.booking'

    meeting_url = fields.Char(string='Enlace de reunión')

    def action_create_google_meet(self):
        if not service_account or not build:
            raise UserError(_('Paquetes de Google API no instalados.'))

        ICP = self.env['ir.config_parameter'].sudo()
        svc_json = ICP.get_param('mb_dd.google_service_account_json')
        calendar_id = ICP.get_param('mb_dd.google_calendar_id', 'primary')
        if not svc_json:
            raise UserError(_('Falta mb_dd.google_service_account_json'))
        info = json.loads(svc_json)
        scopes = ['https://www.googleapis.com/auth/calendar']
        credentials = service_account.Credentials.from_service_account_info(info, scopes=scopes)
        delegated_user = ICP.get_param('mb_dd.google_delegated_user')
        if delegated_user:
            credentials = credentials.with_subject(delegated_user)
        service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
        for b in self:
            start = b.start or fields.Datetime.now() + timedelta(hours=1)
            end = b.stop or (start + timedelta(minutes=int(b.duration or 60)))
            body = {
                'summary': b.appointment_type_id.name or 'Reserva',
                'start': {'dateTime': fields.Datetime.to_string(start)},
                'end': {'dateTime': fields.Datetime.to_string(end)},
                'attendees': [{'email': b.partner_id.email}] if b.partner_id.email else [],
                'conferenceData': {'createRequest': {'requestId': f'odoo-{b.id}', 'conferenceSolutionKey': {'type': 'hangoutsMeet'}}}
            }
            event = service.events().insert(calendarId=calendar_id, body=body, conferenceDataVersion=1).execute()
            hangout = event.get('hangoutLink') or event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri')
            if hangout:
                b.write({'meeting_url': hangout})
        return True

    def open_meet_url(self):
        self.ensure_one()
        if not self.meeting_url:
            return False
        return {'type': 'ir.actions.act_url', 'name': 'Google Meet', 'target': 'new', 'url': self.meeting_url}

    def action_export_stems_csv(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_url', 'url': f'/mb/stems/export/{self.id}', 'target': 'self'}
