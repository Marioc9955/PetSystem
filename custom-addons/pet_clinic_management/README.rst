.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

Pet Clinic / Veterinary Management
==================================

PetSystem's veterinary addon for Odoo 19 Community Edition.

Current status
==============
Source reviewed on 2026-09-14. Module version: ``19.0.1.0.0``.
This is a basic outpatient records application; production readiness has not
been established.

Implemented
-----------
* Pets with type, breed, manually entered age, photo, notes, and an owner linked to an Odoo contact (``res.partner``).
* Appointments with automatic numbering, date/time, reason, and a restricted diagnosis field.
* Treatments linked to appointments, with a date, description, and veterinarian (``res.users``).
* Prescriptions linked to appointments, with medicine lines, dosage schedules, and instructions.
* Vaccination records with administered and next due dates; medicine and vaccine catalogs.
* Standard Odoo forms and lists, plus a pet kanban view. No custom Owl frontend yet.
* A configurable public landing page with original pet artwork, ordered content blocks, admin-only editing, publication rules, and Ecuadorian Spanish translations. See ``LANDING.md`` for setup and verification details.

Access
------
* Receptionist: read, create, and update pets and appointments; no diagnosis access.
* Veterinarian: receptionist access plus clinical records; read-only medicine and vaccine catalogs.
* Administrator: veterinarian access plus catalog management and deletion across addon models.
* Generic internal users: no addon access unless assigned a clinic role.

Permissions are enforced through model access rules and the diagnosis field's
group restriction. Clinical records do not yet have record rules. Landing-page
marketing records have publication record rules. The deployment design is one
database per independent clinic.

Still missing
-------------
* Appointment/clinical completion states, controlled amendments, archival, and medical-history deletion protection.
* Microchip fields and uniqueness checks, and dedicated patient/owner/contact search views.
* An attachment workflow and auditable medical history.
* Email vaccine reminders; a next due date currently only stores information.
* Clinic settings, addon Spanish translations, and verified Ecuador locale/timezone defaults.
* A reception dashboard or patient timeline. A reception dashboard is a proposed first frontend task.

Verification
------------
Tests exist in ``tests/`` for appointment numbering, role permissions, diagnosis
access, and the Odoo 19 pet kanban template. They were inspected, not executed,
during this documentation update. Clean-install, module-upgrade, and browser
workflow results are not established by this review.

Code map
--------
* ``models/``: Python records, relationships, and business logic.
* ``views/``: XML screens, actions, and menus.
* ``security/``: clinic groups and model permissions.
* ``data/``: appointment numbering sequence.
* ``__manifest__.py``: version, dependencies (``base`` and ``web``), and files loaded by Odoo.

See the repository ``README.md`` for local startup instructions.

Configuration
=============
* Assign each clinic user one of the Pet Clinic roles in the user access settings: Receptionist, Veterinarian, or Administrator.
* Receptionists manage pets and appointments. Veterinarians additionally manage clinical records. Administrators manage configuration and deletion.
* Appointment identifiers are generated automatically from the Pet Clinic Appointment sequence.

License
-------
Unresolved upstream inconsistency: ``__manifest__.py`` declares AGPL-3, while
the original declaration below says LGPL-3. An explicit licensing decision is
required before changing declarations or redistributing a modified module.

GNU Lesser General Public License v3.0 (LGPL-3)
(https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

Company
-------
* `Alan Technologies <https://alantechnologies.in>`__

Credits
-------
* Developer: (V18) Jayasuriya
  Contact: alantechnologies.in

Contacts
--------
* Mail Contact : alantechnologies2022@gmail.com
* Website : https://alantechnologies.in

Bug Tracker
-----------
Bugs are tracked on GitHub Issues. In case of trouble, please check there if
your issue has already been reported.

Maintainer
==========
This module is maintained by `Alan Technologies <https://alantechnologies.in/>`__

For support and more information, please visit `Our Website <https://alantechnologies.in/>`__

Further Information
===================
HTML Description: `<static/description/index.html>`__
