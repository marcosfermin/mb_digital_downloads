from odoo import api, fields, models, _
from odoo.exceptions import UserError
import boto3
from botocore.client import Config as BotoConfig

class BookingStems(models.Model):
    _name = 'booking.stems'
    _description = 'Carpeta de stems por reserva'

    booking_id = fields.Many2one('appointment.booking', required=True, ondelete='cascade')
    prefix = fields.Char(required=True, help='Prefijo S3/R2 para esta reserva, p.ej. stems/<booking_id>/')
    total_quota_mb = fields.Integer(string='Cuota total (MB)', help='Cuota máxima total por reserva; si vacío, usa la del tipo de cita o global.')

    def _client(self):
        ICP = self.env['ir.config_parameter'].sudo()
        endpoint_url = ICP.get_param('mb_dd.s3_endpoint_url') or None
        region = ICP.get_param('mb_dd.s3_region') or 'us-east-1'
        access_key = ICP.get_param('mb_dd.s3_access_key')
        secret_key = ICP.get_param('mb_dd.s3_secret_key')
        if not (access_key and secret_key):
            raise UserError(_('Configura claves S3/R2 en Parámetros del Sistema'))
        return boto3.client('s3', region_name=region, endpoint_url=endpoint_url,
                            aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                            config=BotoConfig(signature_version='s3v4'))

    def _bucket(self):
        bucket = self.env['ir.config_parameter'].sudo().get_param('mb_dd.s3_bucket')
        if not bucket:
            raise UserError(_('Falta mb_dd.s3_bucket'))
        return bucket

    def list_objects(self):
        client = self._client()
        bucket = self._bucket()
        all_keys = []
        total_size = 0
        for rec in self:
            resp = client.list_objects_v2(Bucket=bucket, Prefix=rec.prefix)
            contents = resp.get('Contents', []) if resp else []
            keys = []
            for c in contents:
                keys.append(c['Key'])
                total_size += int(c.get('Size') or 0)
            all_keys.append(keys)
        return all_keys, total_size

    def _effective_limits(self):
        ICP = self.env['ir.config_parameter'].sudo()
        max_mb_file_global = int(ICP.get_param('mb_dd.stems_max_mb', '1024'))
        max_mb_total_global = int(ICP.get_param('mb_dd.stems_total_quota_mb', '2048'))
        for rec in self:
            appt = rec.booking_id.appointment_type_id
            max_file = appt.stems_max_mb or max_mb_file_global
            max_total = rec.total_quota_mb or appt.stems_total_quota_mb or max_mb_total_global
            return int(max_file), int(max_total)

    def presign_post(self, filename):
        bucket = self._bucket()
        client = self._client()
        max_file_mb, max_total_mb = self._effective_limits()
        # current total
        _, total_size = self.list_objects()
        remaining_bytes = max(0, (max_total_mb * 1024 * 1024) - total_size)
        if remaining_bytes <= 0:
            raise UserError(_('Has alcanzado la cuota total de esta reserva.'))
        key = f"{self.prefix}{filename}"
        conditions = [
            ["content-length-range", 0, min(remaining_bytes, max_file_mb * 1024 * 1024)],
        ]
        fields_map = {'acl': 'private', 'key': key}
        resp = client.generate_presigned_post(bucket, key, Fields=fields_map, Conditions=conditions, ExpiresIn=3600)
        return resp
