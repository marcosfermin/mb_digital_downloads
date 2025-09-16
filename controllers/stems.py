from odoo import http
from odoo.http import request

class StemsPortal(http.Controller):
    @http.route(['/my/bookings/<int:booking_id>/stems'], type='http', auth='user', website=True)
    def stems_page(self, booking_id, **kw):
        booking = request.env['appointment.booking'].sudo().browse(booking_id)
        if not booking or booking.partner_id != request.env.user.partner_id:
            return request.not_found()
        folder = request.env['booking.stems'].sudo().search([('booking_id','=',booking_id)], limit=1)
        keys = []
        total = 0
        max_mb = int(request.env['ir.config_parameter'].sudo().get_param('mb_dd.stems_max_mb', '1024'))
        max_total_mb = int(request.env['ir.config_parameter'].sudo().get_param('mb_dd.stems_total_quota_mb', '2048'))
        if booking and booking.appointment_type_id:
            if booking.appointment_type_id.stems_max_mb:
                max_mb = int(booking.appointment_type_id.stems_max_mb)
            if booking.appointment_type_id.stems_total_quota_mb:
                max_total_mb = int(booking.appointment_type_id.stems_total_quota_mb)
        if folder:
            listed, total_size = folder.list_objects()
            keys = listed[0] if listed else []
            total = total_size
        return request.render('mb_digital_downloads.portal_stems', {
            'booking': booking,
            'folder': folder,
            'keys': keys,
            'max_mb': max_mb,
            'max_total_mb': max_total_mb,
            'total_uploaded_mb': round(total/1024/1024, 2)
        })

    @http.route(['/my/bookings/<int:booking_id>/stems/presign'], type='json', auth='user')
    def stems_presign(self, booking_id, filename):
        booking = request.env['appointment.booking'].sudo().browse(booking_id)
        if not booking or booking.partner_id != request.env.user.partner_id:
            return {'error': 'not_found'}
        folder = request.env['booking.stems'].sudo().search([('booking_id','=',booking_id)], limit=1)
        if not folder:
            folder = request.env['booking.stems'].sudo().create({'booking_id': booking_id, 'prefix': f'stems/{booking_id}/'})
        resp = folder.presign_post(filename)
        return resp
