# Configurable clinic landing page

## Architecture

This feature lives in `pet_clinic_management`. It adds the native `web` dependency,
two ORM models/tables (`vet.landing.page` / `vet_landing_page` and
`vet.landing.block` / `vet_landing_block`), QWeb rendering and scoped CSS. It does
not require Website, Owl, a second frontend framework or a separate addon.

Each database has one page and its own ordered blocks. Clinic administrators
configure it under **Pet Clinic → Landing Page** using a standard XML form.
The starter page is **unpublished**. Its XML records use `noupdate="1"` so module
upgrades do not reinitialize administrator content.

The form supports a public brand name, logo, hero image and accessible description,
hero copy, contact copy, three color palettes or validated custom colors, and
ordered service cards, image/text blocks (image on either side), and banners.
Each block supports text, an image, an icon and an optional HTTPS/contact button.
The public contact section is explicitly authored marketing content; it does not
read owner records or private company/staff contact information.

## Editing and publishing

1. Save content in **Pet Clinic → Landing Page**.
2. Use **Preview page** (`/pet-clinic/preview`); this requires a clinic administrator.
   Preview includes hidden blocks and carries a no-index directive.
3. Set **Published** and save to make `/pet-clinic` available to visitors.
4. Uncheck **Published** and save to withdraw it. Public requests return 404,
   including requests by logged-in administrators.

Changes to an already published page are immediate. There is no separate staged
revision or revision history. Contact details start empty; replace the starter
marketing copy and add real public contact information before publication.
The CTA scrolls to contact details; this does not implement public appointment booking.

Only administrators can create, write or delete marketing records. Public users,
portal users and other staff can read published marketing records. Global record
rules hide unpublished pages and hide blocks unless both page and block are
published. The public controller uses the public user even for signed-in visitors;
there is no custom `sudo()` path. Existing clinical permissions are unchanged.
Treat every field on a published marketing record as public information.

Text is escaped by QWeb; arbitrary HTML is not accepted. Custom colors require
six-digit hex values and 4.5:1 contrast for the text/background combinations.
Image uploads use Odoo `fields.Image`, dimensions are capped and binaries live in
these dedicated marketing tables. Uploaded artwork itself must remain legible.

## Languages

Odoo 19 lists Ecuadorian Spanish as `es_EC`. Activate it in Odoo to use the included
landing-page translations. The landing defaults to `es_EC` when installed and
otherwise to `en_US`. EN/ES links select installed languages. A clean install
initialized only with Spanish can leave English inactive; activate English too
to offer both languages. Admin-authored copy
uses normal Odoo translated fields. The supplied translations cover this landing
workflow, not the rest of the clinical addon.

## Local verification and startup

Commands below use the existing `.venv` and `.local/odoo.conf`, which are not
committed. Run from the repository root. No dependencies were installed.

The first automatic test-database creation hit a Windows PostgreSQL collation
mismatch. Subsequent test databases were explicitly created with template0,
UTF8 encoding and matching `LC_COLLATE 'C'` / `LC_CTYPE 'C'`, using psycopg2 and
the configured local database role. No databases were deleted.

The original data directory also caused `tempfile.mkstemp` to loop on a session
file permission error. Using a fresh local test data directory resolved the test
login stall; upstream Odoo was not edited. Keep each verification database with
its corresponding data directory below.

Clean installation command used:

```powershell
.venv/Scripts/python.exe odoo-19.0/odoo-bin -c .local/odoo.conf -d pet_clinic_landing_clean_20260915 -i pet_clinic_management --without-demo --load-language=es_EC --test-enable --test-tags /pet_clinic_management --stop-after-init --http-port=8072 --data-dir=.local/landing-clean-data --logfile=.local/landing-clean.log
```

Upgrade/regression command used after correcting the test fixture's language:

```powershell
.venv/Scripts/python.exe -X utf8 odoo-19.0/odoo-bin -c .local/odoo.conf -d pet_clinic_landing_clean_20260915 -u pet_clinic_management --test-enable --test-tags /pet_clinic_management --stop-after-init --http-port=8072 --data-dir=.local/landing-clean-data --logfile=.local/landing-verified-tests.log
```

Synthetic preview database startup command used:

```powershell
.venv/Scripts/python.exe odoo-19.0/odoo-bin -c .local/odoo.conf -d pet_clinic_landing_verify_20260915 --db-filter=^pet_clinic_landing_verify_20260915$ --http-interface=127.0.0.1 --http-port=8071 --data-dir=.local/landing-test-data --logfile=.local/landing-preview.log
```

Only the synthetic preview database was published for visual QA. Its page is at
http://localhost:8071/pet-clinic while that server runs. `pet_clinic_dev` has not
been upgraded or published by this task. Apply the module upgrade to that database
before looking for the new admin menu there.

### Results (2026-09-15)

- Python syntax, XML parsing and `git diff --check` passed.
- An upgrade test run completed with 12 tests, zero failures/errors.
- The final corrected suite also passed on the Spanish-initialized database:
  12 tests, zero failures/errors (`.local/landing-verified-tests.log`).
- Clean installation with `es_EC` completed, but one HTTP test initially failed
  because its fixture assumed English was active on a Spanish-first database.
  The fixture now activates English and explicitly edits `en_US`.
- Spanish seed translations loaded successfully; an ORM assertion verified the
  translated hero title.
- Browser-checked Spanish desktop hero/service cards, English mobile layout at
  390 × 844, and contact-anchor navigation. Both languages rendered correctly.
- Admin browser login was blocked by automatic approval review reporting exhausted
  workspace credits. The admin XML form has been installed/validated by Odoo, and
  authenticated admin preview/role denials have HTTP regression coverage; manual
  editor save/upload/reorder verification remains outstanding.
- Existing duplicate-label warning on prescription medicines remains unrelated.

Original generated artwork and its exact prompt are documented in
`static/src/img/README.md`. No Behance artwork was copied. Existing licensing and
attribution declarations were not changed. This is local development work, not
a production deployment or a production-readiness claim.
