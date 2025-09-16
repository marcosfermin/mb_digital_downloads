# mb_digital_downloads — Odoo 18
**Digital Downloads (S3/R2) – Events & Portal**  
Versión: **18.0.3.1.0**

Este módulo permite gestionar **stems/archivos** asociados a **eventos de calendario** (`calendar.event`) con validaciones de cuota y tamaño, pensado para flujos de **mezcla/master** y entregas digitales a clientes.

> **Nota:** Esta versión **no requiere** el módulo *Appointments* (Enterprise). Si tu instancia tiene `appointment.booking.line`, los *hooks* crearán automáticamente registros de stems por cada evento vinculado a líneas de reserva.

---

## Características
- **Stems por evento**: modelo `mb_dd.stems` anclado a `calendar.event`.
- **Validaciones** de tamaño por archivo y **cuota total** por evento via parámetros del sistema.
- **Vistas de backend**:
  - Menú **Media Bodega → Stems**
  - En formulario de **Evento**:
    - Botón **Stems** (lista vinculada)
    - **Contador** de stems del evento
    - Botón **Crear Google Meet** (placeholder seguro; ver integración abajo)
- **Hooks** pos-instalación: si existe `appointment.booking.line`, crea stems base por evento.
- **Sin dependencias Enterprise obligatorias**.

> Integración con **S3/R2** para pre-firmado y subida: deja los puntos de extensión listos (valida cuotas y campos de metadata). El flujo de subida (controller/JS) puede adaptarse a tu storage.

---

## Compatibilidad
- **Odoo 18** (Community o Enterprise)
- Python 3.10+
- Depende de módulos estándar: `base`, `calendar`, `website`, `website_sale`, `sale_management`, `account`, `portal`, `payment`, `sale_subscription`

---

## Instalación

### Opción A — Odoo.sh
1. Copia el módulo a: `custom/addons/mb_digital_downloads/`
2. Añade `requirements.txt` en la raíz del repo (ver más abajo).
3. En Odoo.sh:
   - Crea un **Staging**
   - **Update Apps List**
   - Instala **Digital Downloads (S3/R2) – Events & Portal**

### Opción B — Docker Compose (dev/prod)
- Monta el módulo en `/mnt/extra-addons/mb_digital_downloads`
- Asegúrate que `addons_path` incluya esa ruta en `odoo.conf`
- Reinicia Odoo y **actualiza el módulo** desde Apps o por CLI:

```bash
# CLI (ejemplo)
odoo -c /etc/odoo/odoo.conf -d <DB> -u mb_digital_downloads --stop-after-init
```

---

## Configuración

### Parámetros del sistema (Settings → Technical → System Parameters)
- `mb_dd.stems_max_mb` — **límite (MB)** por archivo (default: `100`)
- `mb_dd.stems_total_quota_mb` — **cuota total (MB)** por evento (default: `2000`)

> Puedes añadir tus propios parámetros para endpoint/bucket/credenciales (p.ej. `mb_dd.s3_bucket`, `mb_dd.s3_region`, etc.) y usarlos en tu capa de subida/firmado.

### Integración Google Meet (placeholder)
El botón **“Crear Google Meet”** en eventos lanza un `UserError` con mensaje instructivo para evitar estados inconsistentes. Para habilitarlo:
1. Instala las librerías de Google (ya están en `requirements.txt`).
2. Implementa en `models/calendar_event_inherit.py` la función real que:
   - Autoriza con **Service Account** (delegada)
   - Crea el meeting
   - Guarda el enlace en el evento (p. ej. `videocall_location` o campo custom)

---

## Menús / Vistas
- **Menú:** *Media Bodega → Stems*
- **Modelo:** `mb_dd.stems`
- **Evento (calendar.event):**
  - **Botón:** *Stems* → abre lista de stems del evento
  - **Campo calculado:** `mb_stems_count`
  - **Botón:** *Crear Google Meet* (placeholder)

---

## Migración desde una versión previa (anclada a Appointments)
Si tu versión antigua heredaba `appointment.booking`:
- Esta versión **quita** la dependencia de `appointment` y **ancla** los stems a `calendar.event`.
- Si existe `appointment.booking.line`, los *hooks* pos-instalación crearán stems base por cada evento con línea vinculada.

---

## Seguridad y datos
- **No** borra objetos del storage externo en `uninstall_hook` (evita pérdida accidental de archivos).
- Controla permisos con el ACL `access_mb_dd_stems_user` (grupo `base.group_user`). Ajusta según tu flujo.

---

## Desarrollo rápido (puntos de extensión)
- **Validación de cuotas**: método `check_quota_before_upload` en `mb_dd.stems`.
- **Acciones del evento**: métodos `action_mb_open_stems` y `action_create_google_meet` en `calendar.event` (override seguro).
- **Presign/Upload**: agrega controllers/JS para firmar y subir a tu S3/R2.
- **Portal**: puedes añadir templates `website`/`portal` para que el cliente suba/descargue stems.

---

## Soporte
- Autor: Media Bodega / Marcos
- Sitio: https://mediabodega.com
- Licencia: OEEL-1 (ajústala si corresponde)
