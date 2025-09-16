from odoo import http
from odoo.http import request

class BookingPortal(http.Controller):
    @http.route(['/my/bookings'], type='http', auth='user', website=True)
    def my_bookings(self, **kw):
        bookings = request.env['appointment.booking'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)], order='create_date desc')
        return request.render('mb_digital_downloads.portal_my_bookings', {'bookings': bookings})
