from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_subscriber = fields.Boolean(compute='_compute_is_subscriber', store=False)

    def _compute_is_subscriber(self):
        Sub = self.env['sale.subscription']
        for p in self:
            sub = Sub.search([('partner_id','=',p.id), ('recurring_next_date','!=',False), ('stage_category','=','progress')], limit=1)
            p.is_subscriber = bool(sub)
