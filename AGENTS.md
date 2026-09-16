# PetSystem repository guidance

These instructions apply to the repository unless a nested `AGENTS.md` adds compatible, more specific guidance.

## Purpose and current baseline

PetSystem is a veterinary-clinic product built as an Odoo 19 Community Edition addon. The current `custom-addons/pet_clinic_management/` code declares version `19.0.1.0.0`, with `vet.*` models for pets, appointments, treatments, vaccinations, prescriptions, vaccines, and medicines. It has standard Odoo views, role-scoped ACLs, a restricted diagnosis field, and appointment/security/view tests. It still lacks record rules, translations, migrations, clinic configuration, reminders, and an Owl frontend. See the addon's `README.rst` for the current feature and verification status.

The first engineering milestone is a clean, secure Odoo 19 port. Do not treat the downloaded addon as production-ready merely because its XML parses or it installs.

The addon has a licensing inconsistency: `__manifest__.py` says AGPL-3 while `README.rst` says LGPL-3. Preserve the existing author/attribution and obtain an explicit licensing decision before changing license declarations or redistributing a modified module.

## Repository boundaries

- Treat `odoo-19.0/` as read-only upstream reference. It may be searched and run, but never changed to implement PetSystem.
- Put Odoo product behavior in `custom-addons/pet_clinic_management/`. Repository-level setup, scripts, and documentation may live at the root when appropriate.
- Avoid casual changes to the addon name, existing `vet.*` models, data-bearing fields, and XML IDs. Before the first supported/deployed database, a coordinated rename may be made when it clearly improves the design and is covered by a clean-install test. After that point, compatibility changes need a documented and tested migration.
- Use supported Odoo extension mechanisms. A narrowly scoped frontend patch is acceptable only when inheritance, registries, services, widgets, or client actions cannot solve the problem cleanly.
- Do not commit secrets, real clinic data, database dumps, filestores, PostgreSQL data, virtual environments, logs, caches, or machine-specific configuration. Commit safe examples instead.
- Preserve unrelated user changes. Never use destructive Git or filesystem operations without explicit approval.

## Architecture and product scope

- Deploy one shared codebase with one Odoo database per independent clinic/customer. Do not use `clinic_id` or multi-company as the tenant boundary. Multi-company may model branches within one customer later.
- Keep state database-scoped. Avoid process-global caches, shared temporary paths, or jobs that can leak records, settings, branding, or attachments between databases.
- Reuse Odoo concepts where they fit: `res.partner` for owners, `res.users` for staff, `res.company`/settings for clinic identity, and Odoo mail, attachments, products, activities, and scheduled actions. Audit the existing models before replacing or integrating them; avoid parallel sources of truth.
- Target Ecuador first, with `America/Guayaquil` as the default business timezone. Use normal Odoo UTC-aware date handling. The staff experience is Spanish-first, while English must remain usable through standard Odoo translations; verify the supported Ecuadorian Spanish locale rather than hardcoding it.

V1 should remain a coherent outpatient-clinic workflow:

- owners and pets/patients;
- appointments and consultations/treatments;
- vaccination history and due-date tracking;
- prescriptions;
- attachments and auditable medical history;
- email vaccine reminders;
- practical patient/owner/contact/microchip search;
- role-appropriate operational views, with a focused dashboard or patient timeline when they add clear value.

Important domain invariants include unique non-empty microchips per database, archival instead of destructive deletion when history exists, preservation of administered vaccinations and prescriptions, and controlled amendments to completed clinical records. Email reminders must respect opt-out and language, handle missing addresses safely, and be idempotent across retries.

Do not expand V1 into hospitalization, surgery/anesthesia, laboratory or imaging workflows, automatic inventory moves, billing/accounting, SMS/WhatsApp, portals/mobile apps, public booking, multi-branch management, AI clinical advice, or central SaaS provisioning without explicit product approval. Small extension points are fine; speculative infrastructure is not.

## Security, data integrity, and migrations

- Enforce permissions server-side for every model and callable method. Menus, invisible fields, and disabled buttons are not security boundaries.
- Define stable Clinic Administrator, Veterinarian, and Receptionist groups. Generic internal users must not receive PetSystem access automatically. Test the intended create/read/write/delete and state-transition matrix.
- Treat owner contact details and clinical records as confidential. Return, log, export, and email only what the workflow needs.
- Avoid `sudo()`. When a scheduled/system operation genuinely requires it, validate inputs, constrain the record set, document why it is safe, and add a privilege-escalation regression test.
- Use the ORM and server-side constraints. Prefer batch operations, accurate dependencies, actionable translated errors, and explicit indexes for demonstrated search needs. Raw SQL requires a concrete reason, parameterization, and tests.
- Use Odoo attachment access controls; never make clinical uploads public by accident or trust a filename extension as a security check.
- Preserve XML IDs and data-bearing schema for supported databases. Any rename, removal, or semantic change affecting existing data needs an idempotent migration and an upgrade test. The current milestone is a clean Odoo 19 install, not speculative migration of an unknown Odoo 18 production database. Bump the module version intentionally for releases.

## UI and localization

- Use standard Odoo forms, lists, kanban, search, and settings for routine administration. Use Owl for high-frequency or cross-record experiences only when it materially improves the workflow; follow patterns in the local Odoo 19 source and keep server permissions authoritative.
- Do not introduce a second frontend framework without an approved architectural need.
- Make user-facing Python, XML, email, and JavaScript strings translatable. Do not hardcode bilingual copy. Review completed workflows in Spanish and keep English source strings usable.
- Keep custom styles scoped to PetSystem and branding database-configured with validated values. Provide accessible labels, visible focus, sufficient contrast, text in addition to status color, and sensible desktop/tablet behavior.
- Focus RPC endpoints on the minimum authorized payload, batch related data to avoid N+1 calls, and handle loading, empty, and error states without exposing tracebacks or internal paths.

## Development and verification

Before implementation, inspect the relevant addon code and the matching Odoo 19 APIs. The local checkout reports Odoo 19.0 with Python 3.10 as its minimum and PostgreSQL 13 as its minimum. A repository-local `.venv`, `.local/odoo.conf`, and `start.ps1` are present; their presence alone does not establish PostgreSQL availability or successful module installation. The root README records the startup command and prior version check. Verify and document a reproducible local setup before claiming install or integration-test results. Use a repository-local environment and ask before substantial or system-wide dependency installation.

For each change:

1. Make the smallest coherent change that satisfies the requirement; do not edit unrelated files.
2. Add or update tests in proportion to behavior and risk. Security, clinical state, reminders, migrations, and date logic require regression coverage.
3. Run narrow syntax/XML/unit checks first. Run clean-install and module-upgrade tests for porting, schema/security changes, and release candidates once the environment exists; documentation-only changes do not require a full Odoo test run.
4. Use deterministic synthetic data. Include role-denial cases and relevant timezone/date boundaries.
5. Update documentation and configuration examples when behavior or setup changes. Document only commands and outcomes actually verified.
6. Report files changed, decisions, commands run, failures, test results, and remaining risks. Never claim a command passed when it was not run.

Ask before deleting databases or supported data-bearing schema, changing tenant/localization strategy, changing license/attribution, making a compatibility-breaking rename after deployment, adding substantial dependencies, implementing a V1 non-goal, or performing destructive operations.
