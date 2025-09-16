from odoo import api, SUPERUSER_ID

def pre_init_hook(cr):
    pass

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env.registry.get('appointment.booking.line'):
        BL = env['appointment.booking.line']
        Stems = env['mb_dd.stems']
        for bl in BL.search([]):
            ev = bl.calendar_event_id
            if ev and not Stems.search([('calendar_event_id', '=', ev.id)], limit=1):
                Stems.create({'name': f'stems/{ev.id}/', 'calendar_event_id': ev.id})

def uninstall_hook(cr, registry):
    pass
