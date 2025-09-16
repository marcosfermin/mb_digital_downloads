{
    "name": "Digital Downloads (S3/R2) – Events & Portal",
    "summary": "Descargas digitales con URLs firmadas, Stems por evento de calendario, Suscripciones/Club y gating de contenido",
    "version": "18.0.3.1.0",
    "category": "Website/eCommerce",
    "author": "Media Bodega / Marcos",
    "website": "https://mediabodega.com",
    "license": "OEEL-1",
    "depends": [
        "base",
        "calendar",
        "website",
        "website_sale",
        "sale_management",
        "account",
        "portal",
        "payment",
        "sale_subscription"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stems_views.xml",
        "views/calendar_event_views.xml"
    ],
    "assets": {},
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "application": false
}
