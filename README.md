# mb_digital_downloads (Odoo 18 Enterprise)
- Descargas digitales con URLs firmadas (S3/R2)
- Portal /my/downloads
- Stems por reserva: carpeta presignada, límites por archivo y por cuota total
- Reservas/Appointments + Google Meet (API)
- Suscripciones (Club) + Gating /club
- Export CSV de stems (backend, solo equipo)
- Webhook opcional para notificaciones de subida (S3 Event)

## Dependencias Python
```
pip install boto3 google-auth google-auth-oauthlib google-api-python-client
```

## Parámetros del sistema
- mb_dd.s3_bucket, mb_dd.s3_region, mb_dd.s3_endpoint_url, mb_dd.s3_access_key, mb_dd.s3_secret_key
- mb_dd.max_attempts (descargas), mb_dd.url_expiration_seconds
- mb_dd.stems_max_mb (por archivo, global), mb_dd.stems_total_quota_mb (cuota total, global)
- mb_dd.google_service_account_json, mb_dd.google_delegated_user, mb_dd.google_calendar_id
- mb_dd.team_notify_emails (opcional; coma separada)

## S3 Event Notification (opcional)
Configura evento ObjectCreated hacia /mb/stems/webhook (POST JSON). El módulo notificará por email al cliente y al equipo.

## Instalación
Copiar la carpeta `mb_digital_downloads/` al addons_path y actualizar apps. Publicar /club con Website Menus si quieres un enlace en navbar.
