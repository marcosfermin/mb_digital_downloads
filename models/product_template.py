from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_digital = fields.Boolean(
        string='Producto digital',
        help='Si está activo, este producto genera una entrega digital tras el pago.'
    )
    digital_storage_key = fields.Char(
        string='Clave S3/R2 (ZIP/archivo)',
        help='Ruta/clave del objeto en el bucket (p.ej. packs/lofi_guitar_vol1.zip)'
    )
    preview_url = fields.Char(
        string='URL de preview (opcional)',
        help='URL pública (o proxy) para el player de audio/video en el producto.'
    )

    # Opcional: para servicios que generan reservas
    appointment_type_id = fields.Many2one('appointment.type', string='Tipo de cita')
    appointment_duration = fields.Integer(string='Duración (min)', default=60)
