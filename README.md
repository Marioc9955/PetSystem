# PetSystem
Sistema para control de una clínica veterinaria.
Basado en odoo 19 y pet clinic management addon

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
