from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta
import boto3
from botocore.client import Config as BotoConfig

class DigitalDelivery(models.Model):
    _name = 'digital.delivery'
    _description = 'Entrega digital por compra'
    _order = 'create_date desc'

    name = fields.Char(default=lambda self: _('Entrega Digital'))
    order_line_id = fields.Many2one('sale.order.line', required=True, ondelete='cascade')
    order_id = fields.Many2one(related='order_line_id.order_id', store=True)
    partner_id = fields.Many2one(related='order_id.partner_id', store=True)
    product_id = fields.Many2one(related='order_line_id.product_id', store=True)

    storage_key = fields.Char(required=True, help='Clave/objeto en S3/R2')
    url_expires_at = fields.Datetime()
    last_download_at = fields.Datetime()
    attempts_count = fields.Integer(default=0)
    max_attempts = fields.Integer(default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('mb_dd.max_attempts', '5')))
    state = fields.Selection([
        ('available', 'Disponible'),
        ('expired', 'Expirada'),
        ('consumed', 'Consumida'),
    ], default='available', index=True)

    def _get_s3_client(self):
        ICP = self.env['ir.config_parameter'].sudo()
        endpoint_url = ICP.get_param('mb_dd.s3_endpoint_url') or None
        region = ICP.get_param('mb_dd.s3_region') or 'us-east-1'
        access_key = ICP.get_param('mb_dd.s3_access_key')
        secret_key = ICP.get_param('mb_dd.s3_secret_key')
        if not (access_key and secret_key):
            raise UserError(_('Configura claves S3/R2 en Parámetros del Sistema'))
        return boto3.client(
            's3',
            region_name=region,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=BotoConfig(signature_version='s3v4')
        )

    def generate_presigned_url(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError(_('La entrega no está disponible.'))
        if self.attempts_count >= self.max_attempts:
            self.state = 'expired'
            return False

        ICP = self.env['ir.config_parameter'].sudo()
        bucket = ICP.get_param('mb_dd.s3_bucket')
        expires_seconds = int(ICP.get_param('mb_dd.url_expiration_seconds', '172800'))
        if not bucket:
            raise UserError(_('Configura el bucket S3/R2 en Parámetros del Sistema'))

        client = self._get_s3_client()
        try:
            url = client.generate_presigned_url(
                'get_object', Params={'Bucket': bucket, 'Key': self.storage_key}, ExpiresIn=expires_seconds
            )
        except Exception as e:
            raise UserError(_('Error generando URL firmada: %s') % e)

        now = fields.Datetime.now()
        self.write({
            'attempts_count': self.attempts_count + 1,
            'last_download_at': now,
            'url_expires_at': now + timedelta(seconds=expires_seconds),
        })
        return url
