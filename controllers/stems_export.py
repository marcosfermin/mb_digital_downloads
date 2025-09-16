from odoo import http
from odoo.http import request
import csv, io

class StemsExport(http.Controller):
    @http.route(['/mb/stems/export/<int:booking_id>'], type='http', auth='user')
    def export_csv(self, booking_id, **kw):
        if not request.env.user.has_group('mb_digital_downloads.group_mbmusic_team'):
            return request.not_found()
        booking = request.env['appointment.booking'].sudo().browse(booking_id)
        if not booking:
            return request.not_found()
        folder = request.env['booking.stems'].sudo().search([('booking_id','=',booking.id)], limit=1)
        if not folder:
            return request.not_found()
        bucket = request.env['ir.config_parameter'].sudo().get_param('mb_dd.s3_bucket')
        client = folder._client()
        resp = client.list_objects_v2(Bucket=bucket, Prefix=folder.prefix) or {}
        contents = resp.get('Contents', [])
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(['key','size','last_modified','presigned_url'])
        for c in contents:
            key = c['Key']; size = c.get('Size'); lm = c.get('LastModified')
            url = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=900)
            writer.writerow([key, size, lm, url])
        data = out.getvalue().encode('utf-8')
        headers = [('Content-Type', 'text/csv; charset=utf-8'),
                   ('Content-Disposition', f"attachment; filename=stems_booking_{booking.id}.csv")]
        return request.make_response(data, headers=headers)
