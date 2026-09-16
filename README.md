# PetSystem
Sistema para control de una clínica veterinaria.
Basado en Odoo 19 Community Edition y el addon Pet Clinic Management.

## Estado actual

El addon incluye registros básicos de mascotas, citas, tratamientos, vacunas y
recetas, con roles de recepción, veterinario y administrador. La interfaz usa
vistas estándar de Odoo; todavía no hay un frontend personalizado con Owl.
La preparación para producción está pendiente de verificación.

- [Documentación del addon](custom-addons/pet_clinic_management/README.rst): funciones implementadas, permisos, pendientes y estado de pruebas.
- [Guía de desarrollo](AGENTS.md): arquitectura, alcance y reglas del repositorio.

El código del producto vive en `custom-addons/pet_clinic_management/`.
`odoo-19.0/` contiene Odoo y se mantiene sin modificaciones.

## Inicio local (PowerShell)

Con PostgreSQL en ejecución y el entorno local configurado (`.venv`,
`odoo-19.0` y `.local/odoo.conf`), inicia el servidor desde la raíz del proyecto:

```powershell
.\start.ps1
```

El script usa la base de datos existente `pet_clinic_dev`. Abre
[PetSystem local](http://localhost:8069) y usa `Ctrl+C` para detener el servidor.
Para seleccionar otra base de datos existente, usa el parámetro `-Database`.

Verificación realizada: ejecutar `start.ps1 -Version` desde fuera de la raíz
del proyecto devolvió `Odoo Server 19.0` con código de salida 0. Esta comprobación
no inicia el servidor ni verifica la instalación del módulo.
