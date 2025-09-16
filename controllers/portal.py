from odoo import http
from odoo.http import request

class PortalDownloads(http.Controller):
    @http.route(['/my/downloads'], type='http', auth='user', website=True)
    def my_downloads(self, **kw):
        deliveries = request.env['digital.delivery'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)], order='create_date desc')
        return request.render('mb_digital_downloads.portal_my_downloads', {'deliveries': deliveries})
