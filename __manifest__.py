{
    "name": "Digital Downloads (S3/R2) Portal + Bookings + Subscriptions",
    "summary": "Descargas digitales con URLs firmadas, Stems por reserva, Google Meet, Suscripciones y Gating",
    "version": "18.0.2.0.0",
    "category": "Website/eCommerce",
    "author": "Media Bodega / Marcos",
    "website": "https://example.com",
    "license": "OEEL-1",
    "depends": [
        "base",
        "website",
        "website_sale",
        "sale_management",
        "account",
        "portal",
        "payment",
        "appointment",
        "sale_subscription"
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "views/menus.xml",
        "views/product_template_views.xml",
        "views/portal_templates.xml",
        "views/booking_form_button.xml",
        "views/stems_templates.xml",
        "views/appointment_type_views.xml",
        "views/website_club_templates.xml",
        "data/mail_templates.xml",
        "data/subscription_product.xml",
        "data/automation_meet.xml"
    ],
    "assets": {
        "web.assets_frontend": []
    },
    "application": False
}
