from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _mb_create_digital_deliveries(self):
        Delivery = self.env['digital.delivery']
        for order in self:
            for line in order.order_line:
                product = line.product_id.product_tmpl_id
                if product.is_digital and product.digital_storage_key and line.qty_delivered < line.product_uom_qty:
                    Delivery.create({
                        'order_line_id': line.id,
                        'storage_key': product.digital_storage_key,
                    })

    def _mb_handle_service_booking(self):
        Booking = self.env['appointment.booking']
        for order in self:
            for line in order.order_line:
                pt = line.product_id.product_tmpl_id
                if pt.appointment_type_id:
                    booking = Booking.create({
                        'appointment_type_id': pt.appointment_type_id.id,
                        'partner_id': order.partner_id.id,
                        'booked_by_id': order.user_id.id or self.env.user.id,
                        'duration': pt.appointment_duration or 60,
                    })
                    self.env['booking.stems'].create({'booking_id': booking.id, 'prefix': f'stems/{booking.id}/'})

    def action_confirm(self):
        res = super().action_confirm()
        self._mb_create_digital_deliveries()
        self._mb_handle_service_booking()
        return res
