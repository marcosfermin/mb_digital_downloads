from odoo import http
from odoo.http import request
import json

class StemsWebhook(http.Controller):
    @http.route(['/mb/stems/webhook'], type='json', auth='public', csrf=False)
    def stems_webhook(self, **payload):
        # Configure S3 Event Notification to POST here (via API Gateway/Lambda or direct)
        try:
            data = request.httprequest.get_data()
            evt = json.loads(data.decode('utf-8')) if data else payload
        except Exception:
            evt = payload
        # Try to parse records
        records = (evt or {}).get('Records', [])
        Mail = request.env['mail.mail'].sudo()
        for r in records:
            key = r.get('s3', {}).get('object', {}).get('key')
            # Heuristic: stems/<booking_id>/filename
            booking_id = None
            if key and key.startswith('stems/'):
                try:
                    seg = key.split('/')
                    booking_id = int(seg[1])
                except Exception:
                    pass
            if booking_id:
                booking = request.env['appointment.booking'].sudo().browse(booking_id)
                if booking and booking.partner_id and booking.partner_id.email:
                    body = f"Se subió un nuevo archivo de stems: {key}"
                    Mail.create({'email_to': booking.partner_id.email, 'subject': 'Confirmación de subida de stems', 'body_html': f"<p>{body}</p>"}).send()
                    # Notifica al equipo (opcional: lista de correos en parámetro del sistema)
                    team_emails = request.env['ir.config_parameter'].sudo().get_param('mb_dd.team_notify_emails', '')
                    if team_emails:
                        Mail.create({'email_to': team_emails, 'subject': f'Nuevo stem en reserva {booking_id}', 'body_html': f"<p>{body}</p>"}).send()
        return {"ok": True}
