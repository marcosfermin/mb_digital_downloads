from odoo import http
from odoo.http import request

class DownloadController(http.Controller):
    @http.route(['/my/downloads/<int:delivery_id>/get'], type='http', auth='user', website=True)
    def download_signed(self, delivery_id, **kw):
        delivery = request.env['digital.delivery'].sudo().browse(delivery_id)
        if not delivery or delivery.partner_id != request.env.user.partner_id:
            return request.not_found()
        url = delivery.generate_presigned_url()
        if not url:
            return request.render('website.403')
        return request.redirect(url)
